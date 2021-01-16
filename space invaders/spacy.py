import pygame as pg
import math
import random
from pygame import mixer
#initialize
pg.init()

#create the screen
screen = pg.display.set_mode((800,600))

#Title
pg.display.set_caption("space Invaders")

# Icon
icon= pg.image.load("spaceship.png")
pg.display.set_icon(icon)

# Background music
mixer.music.load("spaceinvaders1.mpeg")
mixer.music.play(-1)

# Player
playerimg= pg.image.load("space-invaders.png")
# width of the player
playerX= 350
# height of the player
playerY= 480
playerX_change= 0
playerY_change= 0

# enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[] 
enemyY_change= []
num_of_enemies= 6

for i in range(num_of_enemies):
    enemyimg.append(pg.image.load("enemy1.png"))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.8)
    enemyY_change.append(40)

# bullet
bulletimg= pg.image.load("bullet16.ico")
bulletX= 0
bulletY= 480
bulletX_change= 0
bulletY_change= 2
bullet_state= "ready"
score_val = 0
font = pg.font.Font("freesansbold.ttf", 32)

# Background image
bgimage = pg.image.load("bgimage.jpg")

def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y, i):
    screen.blit(enemyimg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+27,y+5))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance= math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score= font.render("Score: "+ str(score_val), True, (255, 0, 150))
    screen.blit(score, (x,y))

textX= 10
textY= 10

#Game loop
running= True
while running:

    #background color
    screen.fill((0,150,0))

    # background image
    screen.blit(bgimage, (0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running= False

        #check wheter key is pressed or not
        if event.type == pg.KEYDOWN:
            if event.key== pg.K_RIGHT:
                playerX_change += 1
            
            if event.key== pg.K_LEFT:
                playerX_change -= 1

            if event.key== pg.K_UP:
                playerY_change= -0.8
            
            if event.key== pg.K_DOWN:
                playerY_change= 0.8

            if event.key==pg.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound= mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    bulletX= playerX 
                    fire_bullet(bulletX, bulletY)

        if event.type == pg.KEYUP:
            if event.key== pg.K_RIGHT or event.key== pg.K_LEFT or event.key== pg.K_UP or event.key== pg.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # """Player movement direction """
    playerX += playerX_change   
    playerY += playerY_change   

    if playerX >= 730:
        playerX  = 730

    if playerX <= 0:
        playerX  = 0  

    if playerY <= 150:
        playerY  = 150        

    if playerY >= 530:
        playerY  = 530    

    # """ Enemy movement direction """
    for i in range(num_of_enemies):

        

        enemyX[i] += enemyX_change[i]   

        if enemyX[i] >= 730:
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY= 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i]= random.randint(0, 740)
            enemyY[i]= random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state= "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pg.display.update()