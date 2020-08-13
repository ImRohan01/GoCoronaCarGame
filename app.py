import pygame
import time 
import random
from pygame import mixer 

# Initializing 
pygame.init()
screen     = pygame.display.set_mode((600,700))
check      = 0
tm_font    = pygame.font.Font("Gameplay.ttf",100)
start_time = time.time()
pygame.display.set_caption('Go Corona')

#Score coordinates and value
sc_font = pygame.font.Font("Gameplay.ttf",18)
score   = 0
textX   = 260
textY   = 10

#Game over coordinates
go_font   = pygame.font.Font("Gameplay.ttf",32)
gameOverX = 100
gameOverY = 300
game_over = False


#Setting the background for the game window
background  = pygame.image.load('img/road.jpg').convert()
background1 = pygame.transform.scale(background, (400, 700))
background2 = pygame.transform.scale(background, (400, 700))
rect1       = background1.get_rect()
rect1       = rect1.move(100,0)
rect2       = background2.get_rect()
rect2       = rect2.move(100,-700)
bspeed      = 0
pspeed      = 0

#Getting the car onto the road
playerImg = pygame.image.load('img/car.png')
playerImg = pygame.transform.scale(playerImg, (125, 150))
playerX   = 135
playerY   = 525
position  = "left"

#Coins and obstacles
left_arr  = []
right_arr = []
coin      = pygame.image.load('img/coin.png')
coin      = pygame.transform.scale(coin, (40, 40))
barrier   = pygame.image.load('img/virus.png')
barrier   = pygame.transform.scale(barrier, (40, 40))
items     = [coin,barrier]
sides     = [left_arr,right_arr]

def player(playerX,playerY):
    screen.blit(playerImg,(playerX,playerY))

def addItem(arr,pos,ps):
    i = 0 
    while(i<len(arr)):
        arr[i][1] += 0.5 + ps
        screen.blit(arr[i][0],(pos,arr[i][1]))
        if arr[i][1] > 700:
            arr.remove(arr[i])
        else:
            i += 1

def gameOver(x,y):
    game_over_value = go_font.render('STAY HOME, STAY SAFE', True, (255,255,255))
    screen.blit(game_over_value, (x,y))

def showScore(x,y):
    score_value = sc_font.render("SCORE : " + str(score), True, (255,255,255))
    screen.blit(score_value, (x,y))

def startTimer(check):
    if check == 1:
        for i in range(3):
            count = tm_font.render(str(i+1), True, (255,255,255))
            screen.blit(count, (275,300))
            st = time.time()
            pygame.display.update()
            while(time.time()-st < 1):
                pass
            count = None
        bg_sound = mixer.Sound("sounds/background.wav")
        bg_sound.play(-1)

while True:
    screen.fill((0,255,0))
    screen.blit(background1,rect1)
    screen.blit(background2,rect2)
    rect1 = (100, bspeed)
    rect2 = (100,-700 + bspeed)
    bspeed += 0.5 + pspeed
    if  bspeed > 700:
        rect1 = (100,0)
        rect2 = (100,-700)
        bspeed = 0

    #Start countdown
    startTimer(check)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and position == "right":
                position = "left"
            if event.key == pygame.K_RIGHT and position == "left":
                position = "right"
        
    if game_over:
        left_arr  = []
        right_arr = []
        gameOver(gameOverX,gameOverY)
    
    if time.time() - start_time > (1 - pspeed*(0.7)):
        start_time = time.time()
        idx  = random.randint(0,1)
        item = items[idx]
        side = sides[random.randint(0,1)]
        side.append([item,-50, idx])

    #Items display
    if not game_over:
        addItem(left_arr,177,pspeed)
        addItem(right_arr,382,pspeed)

    #Check coin collected
    for i in range(len(right_arr)):
        if right_arr[i][1] > 525 and right_arr[i][1] < 660 and playerX+100>382:
            right_arr[i][1] = 1000
            if right_arr[i][2] == 0:
                coin_sound = mixer.Sound("sounds/coin.wav")
                coin_sound.play()
                score += 1
            else:
                game_over = True
                go_sound  = mixer.Sound("sounds/gameover.wav")
                go_sound.play()
            print(score)

    for i in range(len(left_arr)):
        if left_arr[i][1] > 525 and left_arr[i][1] < 660 and playerX<177:
            left_arr[i][1] = 1000
            if left_arr[i][2] == 0:
                coin_sound = mixer.Sound("sounds/coin.wav")
                coin_sound.play()
                score += 1
            else:
                game_over = True
                go_sound  = mixer.Sound("sounds/gameover.wav")
                go_sound.play()
            print(score)
            
    if position == "left" and playerX > 135:
        playerX -= 0.5
    elif position == "right"and playerX < 340:
        playerX += 0.5
    else:
        playerX = 340 if position=="right" else 135
    if score%5 == 0:
        pspeed = 0.1*(score//5)

    showScore(textX,textY)
    player(playerX,playerY)
    pygame.display.update()
    check += 1

