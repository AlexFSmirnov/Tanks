

def start_menu():   
    def drawTanksSelect(selected_1, selected_2):
        for team in tanks_left:
            tank = openImage("tanks/tank_" + team + ".png")
            pc = pixCords(*tanks_left[team])
            if checkMouseInBlock(mouse_pos, pc, 1) and mouse_buttons[0] and team != selected_2:
                selected_1 = team    
            if team == selected_1:
                draw.rect(tank, (255,0,0), (0, 0, CELL_SIDE, CELL_SIDE), 3)
            screen.blit(tank, pc)
            
            tank = openImage("tanks/tank_" + team + ".png")    
            pc = pixCords(*tanks_right[team])
            if checkMouseInBlock(mouse_pos, pc, 1) and mouse_buttons[0] and team != selected_1:
                selected_2 = team 
            if team == selected_2:
                draw.rect(tank, (255,0,0), (0, 0, CELL_SIDE, CELL_SIDE), 3)        
            screen.blit(tank, pc) 
        return (selected_1, selected_2)
            
    tanks_left = {"red":[10, 12], "green":[12, 12], "blue":[14, 12], "white":[16, 12]}
    tanks_right = {"red":[34, 12], "green":[36, 12], "blue":[38, 12], "white":[40, 12]}
    
    selected_1 = None
    selected_2 = None
    
    #Opening level
    level_name = "start_menu"
    level = loadLevel("config/" + level_name + ".txt")
    
    updateLevel(full=True)
    
    clock = pygame.time.Clock()
    
    p1_name = InputBox(pixCords(2, 15)[0], pixCords(2, 15)[1], 22, value="Player1")
    p2_name = InputBox(pixCords(27, 15)[0], pixCords(27, 15)[1], 22, value="Player2")
    
    p1_name.update()
    while True:    
        clock.tick(10)
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get(): 
            if e.type == QUIT:
                os._exit(0)
        print(getCords(mouse_pos[0], mouse_pos[1]))
              
        screen.blit(bg, (0,0))  
        (selected_1, selected_2) = drawTanksSelect(selected_1, selected_2)
        p1_name.update()
        p2_name.update()
        pygame.display.update()     