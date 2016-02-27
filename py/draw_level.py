def openImage(path, scaleX=CELL_SIDE, scaleY=CELL_SIDE, angle=0):
    img = pygame.image.load("images/" + path) 
    img = pygame.transform.scale(img, (scaleX, scaleY))
    img = pygame.transform.rotate(img, angle)
    return img

def drawCell(x, y, typ, surf=False, pix=0):
    global map_screen
    global tank_screen
    global score_screen
    
    if not surf: surf = map_screen
    if pix: x, y = getCords(x, y)
    xp, yp = pixCords(x, y)
    block = openImage(BLOCK_TYPES[typ])
    surf.blit(block, (xp, yp))


def updateLevel(x=0, y=0, r=0, full=False, cur=False, pix_cords=False):
    rx, ry = r, r
    if pix_cords: 
        x, y = getCords(x, y)
    if full:
        for y0 in range(CELL_H):
            for x0 in range(CELL_W):
                drawCell(x0, y0, level[y0][x0])
        screen.blit(score_screen, (0,0))        
        return
    for y0 in range(y - ry, y + ry + 1):
        for x0 in range(x - rx, x + rx + 1):
            if x0 != x or y0 != y or cur:
                if (y0 < len(level) and x0 < len(level[0])): drawCell(x0, y0, level[y0][x0])
                else: drawCell(x0, y0, " ")  