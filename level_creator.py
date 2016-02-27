from random import randint
from random import choice
from time import sleep
from pygame import *
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
        level[i] = list(level[i].strip())
    return level

def saveLevel(level, path):
    fout = open("levels/" + path + ".txt", 'w')
    for line in level:
        fout.write(''.join(line) + '\n')

def pixCords(x, y):
    return (CELL_SIDE * x, CELL_SIDE * y)
def getCords(x, y):
    return (x // CELL_SIDE, y // CELL_SIDE)


def drawCursor(x, y, typ, pix=0):
    if pix: x, y = getCords(x, y)
    xp, yp = pixCords(x, y)
    block = pygame.image.load("images/" + BLOCK_TYPES[typ]) 
    draw.rect(block, (255, 0, 0), (0, 0, 15, 15), 2)
    screen.blit(block, (xp, yp))

def genRandomMaze():
    global level
    nw = (CELL_W + 1) // 2
    nh = (CELL_H) // 2
    maze = maze_gen(nw, nh)
    level = [["D"] * CELL_W for i in range(CELL_H)]
    for y in range(1, nh):
        for x in range(1, nw):
            if maze[y][x].bottom: 
                level[y * 2][x * 2 - 1] = "-" 
                if x != nw - 1: level[y * 2][x * 2] = "-" 
                level[y * 2][x * 2 - 2] = "-" 
            if maze[y][x].right and x != nw - 1: 
                level[y * 2 - 1][x * 2] = "-"   
                level[y * 2][x * 2] = "-" 
                level[y * 2 - 2][x * 2] = "-" 
    level[0][0] = "D"   
    level[-1][-1] = "D"
    updateLevel(full=True)
    

#config 
exec(open("config/config.txt").read())
exec(open("config/block_types.txt").read())
exec(open("py/classes.py").read())
exec(open("py/draw_level.py").read())
exec(open("py/maze_gen.py").read())
exec(open("py/textlib.py").read())

#--CONSTANTS-------------------------------------------------------------------#
#Display                                                                       #
WIND_W = CELL_W * CELL_SIDE                                                    #
WIND_H = CELL_H * CELL_SIDE                                                    #
DISPLAY = (WIND_W, WIND_H)                                                     #
BACKGROUND_COLOR = "#FFFFFF"                                                   #
#------------------------------------------------------------------------------#



#--INIT-------------------------------------------------------------------------
pygame.init() 
try:
    seticon('icon.ico')
except:
    print("Sorry, no icon for you.")
screen = pygame.display.set_mode(DISPLAY) 
pygame.display.set_caption("Tanks") 
map_screen = Surface((WIND_W, WIND_H))
map_screen.fill(Color(BACKGROUND_COLOR))
score_screen = Surface((0,0))
tanks_screen = Surface((0,0))
pygame.mouse.set_visible(False)
#-------------------------------------------------------------------------------

prev_buttons = pygame.mouse.get_pressed()
selected = "-"
drawLine = False
level_name = "Untitled"
is_saved = ""
level = loadLevel("levels/" + level_name + ".txt")
updateLevel(full=True)
while True:   
    pygame.display.set_caption(level_name + is_saved) 
    for e in pygame.event.get(): 
        if e.type == QUIT:
            os._exit(0)
            
    keys_pressed = key.get_pressed()
    pos_pix = pygame.mouse.get_pos()
    pos = getCords(pos_pix[0], pos_pix[1])  
    cur_buttons = pygame.mouse.get_pressed()    
    
    #KEY SHORTCUTS---------------------------------------------------------------------------------------------------------------#
    if keys_pressed[K_s] and ((keys_pressed[K_LCTRL] and keys_pressed[K_LSHIFT]) or level_name == "Untitled"):  # Saving a copy  #
        level_name = inputText(10, 10, 20)                                                                                       #
        saveLevel(level, level_name)                                                                                             #
                                                                                                                                 #
    if keys_pressed[K_s] and keys_pressed[K_LCTRL]:  # Saving                                                                    #
        is_saved = ""                                                                                                            #
        saveLevel(level, level_name)                                                                                             #
                                                                                                                                 #
    if keys_pressed[K_n] and keys_pressed[K_LCTRL]:  # Creating new                                                              #
        is_saved = ""                                                                                                            #
        level_name = "Untitled"                                                                                                  #
        level = [["D"] * CELL_W for i in range(CELL_H)]                                                                          #
        updateLevel(full=True)                                                                                                   #
                                                                                                                                 #
    if keys_pressed[K_o] and keys_pressed[K_LCTRL]:  # Opening                                                                   #
        prevname = level_name                                                                                                    #
        level_name = inputText(10, 10, 20)                                                                                       #
        try:                                                                                                                     #
            level = loadLevel("levels/" + level_name + ".txt")                                                                   #
            is_saved = ""                                                                                                        #
        except:                                                                                                                  #
            print("No such file")                                                                                                #
            level_name = prevname                                                                                                #
        updateLevel(full=True)                                                                                                   #
                                                                                                                                 #
    if keys_pressed[K_r] and keys_pressed[K_LALT]:  # Generating random maze                                                     #
        genRandomMaze()                                                                                                          #
        is_saved = "*"                                                                                                           #
                                                                                                                                 #
    if keys_pressed[K_c] and keys_pressed[K_LALT]:  # Clearing                                                                   #
        level = [["D"] * CELL_W for i in range(CELL_H)]                                                                          #
        is_saved = "*"                                                                                                           #
    #----------------------------------------------------------------------------------------------------------------------------#
                                                                                                                                 
    
    #MOUSE CLICKS----------------------------------------------------------------------------------------------------------------#
    if cur_buttons[0]: is_saved = "*"                                                                                            #
                                                                                                                                 #
    if cur_buttons[0] and not keys_pressed[K_LSHIFT]:  # Drawing cell                                                            #
        level[pos[1]][pos[0]] = selected                                                                                         #
    if cur_buttons[2] and not prev_buttons[2] and not keys_pressed[K_LSHIFT]:  # Scrolling through block types                   #
        selected = TYPES_LIST[TYPES_LIST.index(selected) - 1]                                                                    #
    if cur_buttons[1] and not prev_buttons[1] and not keys_pressed[K_LSHIFT]:  # Selecting the block that is on focus            #
        selected = level[pos[1]][pos[0]]                                                                                         #
                                                                                                                                 #
    #Drawing line                                                                                                                #
    if cur_buttons[0] and not prev_buttons[0] and keys_pressed[K_LSHIFT]:                                                        #
        drawLine = (pos[0], pos[1])                                                                                              #
    if not cur_buttons[0] and prev_buttons[0] and drawLine != False:                                                             #
        if abs(drawLine[0] - pos[0]) < abs(drawLine[1] - pos[1]):                                                                #
            for i in range(min(drawLine[1], pos[1]), max(drawLine[1], pos[1]) + 1):                                              #
                drawCell(drawLine[0], i, selected)                                                                               #
                level[i][drawLine[0]] = selected                                                                                 #
        if abs(drawLine[0] - pos[0]) > abs(drawLine[1] - pos[1]):                                                                #
            for i in range(min(drawLine[0], pos[0]), max(drawLine[0], pos[0]) + 1):                                              #
                drawCell(i, drawLine[1], selected)                                                                               #
                level[drawLine[1]][i] = selected                                                                                 #
        drawLine = False                                                                                                         #
    #----------------------------------------------------------------------------------------------------------------------------#
    
    
    #Updating screen        
    drawCell(pos[0], pos[1], level[pos[1]][pos[0]])    
    screen.blit(map_screen, (0,0))
    drawCursor(pos[0], pos[1], selected)
    prev_buttons = cur_buttons
    pygame.display.update()     