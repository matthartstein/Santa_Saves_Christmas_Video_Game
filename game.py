# Imports
import random
import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen = set_mode requires a tuple as argument; width | height in pixels
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Home screen
#home = pygame.image.load("home.jpg")

# Background music
mixer.music.load("music.wav")
mixer.music.play(-1)

# Set program title and icon
pygame.display.set_caption("The Best Game Ever!")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png") # Load sprite image
playerX = 375   # Load at this x value
playerY = 480   # Load at this y value
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change= []
enemyY_change = []
num_enemies = 3

# Items
itemImg = []
itemX = []
itemY = []
itemX_change= []
itemY_change = []
num_items = 3

# Number of enemies
for i in range(num_enemies):
    enemyImg.append(pygame.image.load("elf.png"))
    enemyImg.append(pygame.image.load("grinch.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 600))
    enemyX_change.append(1)
    enemyY_change.append(1)
    
# Number of health items
for a in range(num_items):
    itemImg.append(pygame.image.load("cookie.png"))
    itemX.append(random.randint(0, 800))
    itemY.append(random.randint(0, 600))
    itemX_change.append(1)
    itemY_change.append(1)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 710
textY = 575

# Health
health_value = 100
font = pygame.font.Font('freesansbold.ttf', 20)
fontX = 10
fontY = 575

# Game over text
game_over = pygame.font.Font('freesansbold.ttf', 64)

def displayScore(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))
    
def displayHealth(x, y):
    health = font.render("Health: " + str(health_value), True, (0, 0, 0))
    screen.blit(health, (x, y))
    
def gameOver():
    text = font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(text, (350, 300))
    mixer.music.stop()

def player(x, y):   # Send in the new coordinate values we want to load the next image at
    screen.blit(playerImg, (x, y)) # Draw an image onto the screen (surface)
    
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
    
def cookie(x, y, i):
    screen.blit(itemImg[i], (x, y))
    
def isCollision(enemyX, enemyY, playerX, playerY):
    global health_value
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance < 20:
        health_value -= 10
        return True
    else:
        return False
    
# Game loop = Allow the screen to continuously run until event ends or user quits
running = True
while running:
    # Set background color; argument is a tuple; RBG values as arguments
    screen.fill((0, 0, 0))  # But the screen doesn't "update" yet; no change
    
    # Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():    # Keep the screen running until an event
        if event.type == pygame.QUIT:
            running = False
            
        # If any keystroke is pressed, check whether its right or left/up or down
        if event.type == pygame.KEYDOWN: # Means a key has been pressed on computer
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0  # Stop moving sprite on release
                playerY_change = 0  # Stop moving sprite on release
                
    # Player movement with boundaries
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
        if playerY <= 0:
            playerY = 0
        if playerY >= 550:
            playerY = 550
    elif playerX >= 750:
        playerX = 750
        if playerY <= 0:
            playerY = 0
        if playerY >= 550:
            playerY = 550
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 550:
        playerY = 550
    else:
        pass
    
    # Enemy Movement
    for i in range(num_enemies):
        
        # Game over
        if health_value == 0:
            for j in range(num_items):
                enemyY[j] = 2000
                itemY[j] = 2000
            gameOver()
            break
        
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            if enemyY[i] <= 0:
                enemyY[i] = 0
            if enemyY[i] >= 550:
                enemyY[i] = 550
        elif enemyX[i] >= 750:
            enemyX_change[i] = -1
            if enemyY[i] <= 0:
                enemyY[i] = 0
            if enemyY[i] >= 550:
                enemyY[i] = 550
        elif enemyY[i] <= 0:
            enemyY_change[i] = 1
        elif enemyY[i] >= 550:
            enemyY_change[i] = -1
        
        # Enemy Collision
        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:
            score_value += 1
            attack_sound = mixer.Sound('attack.wav')
            attack_sound.play()
            enemyX[i] = random.randint(0, 800)   # Load at this x value
            enemyY[i] = random.randint(0, 600)   # Load at this y value
            
        enemy(enemyX[i], enemyY[i], i)
        
        # Item collision
        item_collision = isCollision(itemX[i], itemY[i], playerX, playerY)
        if item_collision:
            health_value = 100
            slurp = mixer.Sound('slurp.wav')
            slurp.play() 
            
        cookie(itemX[i], itemY[i], i)
    
    # Call player method after screen.fill or it will not appear on the screen!
    # Screen = Drawn First
    # Player = Drawn Second; we draw the player on top of the screen (surface), so
    #          we call screen.fill before anything else; drawing sprites occurs after
    player(playerX, playerY)
    
    # Show score
    displayScore(textX, textY)
    
    # Show Health
    displayHealth(fontX, fontY)
    
    # Update and display any changes made to the screen before looping again
    pygame.display.update()