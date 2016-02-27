from random import randint
from random import choice
from time import sleep
from pygame import *
import math
import pygame  
import sys
import os           
        
    
def seticon(iconname):
    icon=pygame.Surface((32,32))
    icon.set_colorkey((0,0,0))#and call that color transparant
    rawicon=pygame.image.load(iconname)#must be 32x32, black is transparant
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)#set wind
    
def loadLevel(path):
    level = open(path).readlines()
    for i in range(len(level)):
        level[i] = list(level[i].strip() + "-")
    return level + [["-"] * (CELL_W + 2)]

def pixCords(x, y):
    return (CELL_SIDE * x, CELL_SIDE * y)
def getCords(x, y):
    return (x // CELL_SIDE, y // CELL_SIDE)
              

#config 
exec(open("config/config.txt").read())
exec(open("config/block_types.txt").read())
exec(open("config/keybinds.txt").read())
exec(open("config/cheats.txt").read())
exec(open("py/draw_level.py").read())
exec(open("py/classes.py").read())
exec(open("py/textlib.py").read())

#--CONSTANTS-------------------------------------------------------------------#
#Display                                                                       #
WIND_W = CELL_W * CELL_SIDE                                                    #
WIND_H = CELL_H * CELL_SIDE                                                    #
DISPLAY = (WIND_W, WIND_H)                                                     #
BACKGROUND_COLOR = "#FFFFFF"                                                   #
#Teams                                                                         #
GREEN = "green"                                                                #
RED = "red"                                                                    #
BLUE = "blue"                                                                  #
WHITE = "white"                                                                #
YELLOW = "yellow"                                                              #
#Directions                                                                    #
UP = 1                                                                         #
LEFT = 90                                                                      #
DOWN = 180                                                                     #
RIGHT = 270                                                                    #
#Other                                                                         #
BULLET_SIDE = CELL_SIDE // 8 * 3                                               #
if MOVEMENT_SPEED == -1: MOVEMENT_SPEED = CELL_SIDE // 3                       #
if ROTATING_SPEED == -1: ROTATING_SPEED = MOVEMENT_SPEED * 2                   #
if BULLET_SPEED == -1: BULLET_SPEED = MOVEMENT_SPEED * 2                       #
#------------------------------------------------------------------------------#

#Opening level
level_name = "level_1"
level = loadLevel("levels/" + level_name + ".txt")

#Generating players
p1_team = RED
p1 = Tank(p1_team, 0, 0)

p2_team = GREEN
p2 = Tank(p2_team, WIND_W - CELL_SIDE, WIND_H - CELL_SIDE, angle=180)

bullets = []


#Generating team:player
team_player = {p1_team:p1, p2_team:p2} 


#--INIT------------------------------------------------------------------------#
pygame.init()                                                                  #
try:                                                                           #
    seticon('icon.ico')                                                        #
except:                                                                        #
    print("Sorry, no icon for you.")                                           #
screen = pygame.display.set_mode(DISPLAY)                                      #
pygame.display.set_caption("Tanks")                                            #
bg = Surface((WIND_W, WIND_H))                                                 #
bg.fill(Color(BACKGROUND_COLOR))                                               #
#------------------------------------------------------------------------------#


drawLevel()
clock = pygame.time.Clock()
while True:    
    clock.tick(30)
    for e in pygame.event.get(): 
        if e.type == QUIT:
            os._exit(0)
        if e.type == KEYDOWN:
            #Shooting----------------------------------------------------------#  This block will exec only once per button press
            tmp = (CELL_SIDE - BULLET_SIDE) // 2                               #
            #Player1                                                           #1
            if e.key == P1_FIRE:                                               #1
                bullets.append(Bullet(p1.x + tmp, p1.y + tmp, p1.an))          #1
                bullets[-1].move()                                             #1
            #Player2                                                           #2
            if e.key == P2_FIRE:                                               #2
                bullets.append(Bullet(p2.x + tmp, p2.y + tmp, p2.an))          #2
                bullets[-1].move()                                             #2
            #------------------------------------------------------------------#
    keys_pressed = key.get_pressed()
            
        
    #Player1-movement----------------------------------------------------------#1
    if keys_pressed[P1_UP]:  # Moving                                          #1
        p1.moving = UP                                                         #1
    elif keys_pressed[P1_DOWN]:                                                #1
        p1.moving = DOWN                                                       #1
    else:                                                                      #1
        p1.moving = False                                                      #1
                                                                               #1
    if keys_pressed[P1_LEFT]:  # Rotating                                      #1
        p1.rotating = LEFT                                                     #1
    elif keys_pressed[P1_RIGHT]:                                               #1
        p1.rotating = RIGHT                                                    #1
    else:                                                                      #1
        p1.rotating = False                                                    #1
    #--------------------------------------------------------------------------#1
    
    #Player2-movement----------------------------------------------------------#2
    if keys_pressed[P2_UP]:  # Moving                                          #2
        p2.moving = UP                                                         #2
    elif keys_pressed[P2_DOWN]:                                                #2
        p2.moving = DOWN                                                       #2
    else:                                                                      #2
        p2.moving = False                                                      #2
                                                                               #2
    if keys_pressed[P2_LEFT]:  # Rotating                                      #2
        p2.rotating = LEFT                                                     #2
    elif keys_pressed[P2_RIGHT]:                                               #2
        p2.rotating = RIGHT                                                    #2
    else:                                                                      #2
        p2.rotating = False                                                    #2
    #--------------------------------------------------------------------------#2
    
    
    if keys_pressed[INSERT_CHEAT]:  # Check for cheats
        cheat = inputText(10, 10, 20)
        drawLevel()
        checkCheat(cheat)      
    
    if keys_pressed[K_o] and keys_pressed[K_LCTRL]:  # Opening a new level
        level_name = inputText(10, 10, 20)
        try:
            level = loadLevel("levels/" + level_name + ".txt")
        except:
            print("No such file")
        p1.x, p1.y = (0, 0)
        p1_bullets = []
        updateLevel(full=True)      
            
              
    screen.blit(bg, (0,0))  
    
    p1.update()
    p2.update()
    
    updateBullets()
            
    pygame.display.update()     