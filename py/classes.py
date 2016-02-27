class Tank:
    def __init__(self, team, x, y, angle=0):
        self.team = team
        self.x = x
        self.y = y
        self.an = angle
        self.moving = False
        self.rotating = False
        self.mcd = MOVEMENT_COOLDOWN
        self.godmode = False
        self.dead = 0
    
    def check(self, dr, sn, cs):
        x = self.x + round(cs * MOVEMENT_SPEED)
        y = self.y - round(sn * MOVEMENT_SPEED)
        tg = True
        for i in range(CELL_SIDE):
            for j in range(CELL_SIDE):
                nx, ny = getCords(x + i, y + j)
                if level[ny][nx] in WALLS:
                    tg = False
                for team in team_player.keys():
                    player = team_player[team]
                    if self.team != team:
                        p1x1, p1y1, p1x2, p1y2 = x, y, x + CELL_SIDE, y + CELL_SIDE
                        p2x1, p2y1, p2x2, p2y2 = player.x, player.y, player.x + CELL_SIDE, player.y + CELL_SIDE
                        if p1x1 < p2x2 and p2x1 < p1x2 and p1y1 < p2y2 and p2y1 < p1y2:  # DEBUG IT, BITCH!
                            tg = False
        return tg
    
    def checkDeath(self):
        death = True
        for i in range(CELL_SIDE):
            for j in range(CELL_SIDE):
                nx, ny = getCords(self.x + i, self.y + j)
                try: 
                    if level[ny][nx] not in DEADLY:
                        death = False
                except: pass
        if death:
            self.dead = 1
 
    def checkCooldown(self):
        if self.mcd == 0: self.mcd = MOVEMENT_COOLDOWN
        else: self.mcd -= 1
    
    def draw(self):
        xp, yp = getCords(self.x, self.y)
        tank = openImage("tanks/tank_" + self.team + ".png", angle = self.an - 90)
        tank_screen.blit(tank, (self.x, self.y))  
        
    
    def rotate(self):
        if not self.mcd and self.rotating == LEFT:
            self.an += ROTATING_SPEED
        if not self.mcd and self.rotating == RIGHT:
            self.an -= ROTATING_SPEED
        self.an %= 360
    
    def move(self):
        sn = math.sin((self.an) / 180 * math.pi)
        cs = math.cos((self.an) / 180 * math.pi)
        if self.moving == UP and not self.mcd:
            if self.check(UP, sn, cs) or self.godmode:
                self.x += round(cs * MOVEMENT_SPEED)
                self.y -= round(sn * MOVEMENT_SPEED)       
            elif self.check(UP, 0, cs):
                self.x += round(cs * MOVEMENT_SPEED)
            elif self.check(UP, sn, 0):
                self.y -= round(sn * MOVEMENT_SPEED)  
        if self.moving == DOWN and not self.mcd:
            if self.check(DOWN, -sn, -cs) or self.godmode:
                self.x -= round(cs * MOVEMENT_SPEED)
                self.y += round(sn * MOVEMENT_SPEED)       
            elif self.check(DOWN, 0, -cs):
                self.x -= round(cs * MOVEMENT_SPEED)
            elif self.check(DOWN, -sn, 0):
                self.y += round(sn * MOVEMENT_SPEED)   
                
    def explode(self):
        explosion = openImage("weapons/explosion.png", scaleX = CELL_SIDE * 4)
        step = self.dead // 2
        
        exp_step = Surface((CELL_SIDE, CELL_SIDE))  # Creating the Sufrace for the current step of explosion
        exp_step.fill((0,0,0))  # Filling it with black
        exp_step.set_colorkey((0,0,0))  # And changing black into transparent
        
        exp_step.blit(explosion, (0,0), (step * CELL_SIDE, 0, CELL_SIDE, CELL_SIDE))  # Bliting the explosion step on this surface
        exp_step = pygame.transform.rotate(exp_step, self.an - 90)  # Rotating the image
        
        tank_screen.blit(exp_step, (self.x, self.y))  # Bliting curent step on the main tank_screen
    
    def update(self):
        if not self.dead:
            self.checkCooldown()
            self.rotate()
            self.move()
            self.draw()
            self.checkDeath()
        if self.dead:
            self.explode()
            if self.dead < 6: self.dead += 1


class Bullet:
    def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.an = angle
            self.lft = BULLET_LIFETIME
        
    def check(self, sn, cs):  # Returns True if it is not possible to travel to this vector on a new iteration
        x = self.x + round(cs * BULLET_SPEED)
        y = self.y - round(sn * BULLET_SPEED)
        tg = False
        for i in range(BULLET_SIDE):
            for j in range(BULLET_SIDE):
                nx, ny = getCords(x + i, y + j)
                if level[ny][nx] in WALLS:
                    tg = True
        return tg
    
    def changeAngle(self):
        sn = math.sin((self.an) / 180 * math.pi)
        cs = math.cos((self.an) / 180 * math.pi)  
        if self.check(sn, 0):
            sn = -sn
            self.an = (-self.an) % 360
        if self.check(0, cs):
            cs = -cs
            self.an = (180 - self.an) % 360
        return(sn, cs)
    
    def checkKill(self):
        for team in team_player.keys():
            player = team_player[team]
            if self.x + BULLET_SIDE // 2 in range(player.x, player.x + CELL_SIDE) and self.y + BULLET_SIDE // 2 in range(player.y, player.y + CELL_SIDE) and not player.godmode:
                player.dead = 1
                self.lft = -10
    
    def draw(self):
        xp, yp = getCords(self.x, self.y)
        bullet = openImage("weapons/bullet.png", BULLET_SIDE, BULLET_SIDE, self.an - 90) 
        tank_screen.blit(bullet, (self.x, self.y)) 
    
    def move(self):
        sn, cs = self.changeAngle()
        self.x += round(cs * BULLET_SPEED)
        self.y -= round(sn * BULLET_SPEED) 
    
    def explode(self):
        explosion = openImage("weapons/explosion.png", scaleX = CELL_SIDE * 4)
        step = abs(self.lft) // 2
        
        exp_step = Surface((CELL_SIDE, CELL_SIDE))  # Creating the Sufrace for the current step of explosion
        exp_step.fill((0,0,0))  # Filling it with black
        exp_step.set_colorkey((0,0,0))  # And changing black into transparent
        
        exp_step.blit(explosion, (0,0), (step * CELL_SIDE, 0, CELL_SIDE, CELL_SIDE))  # Bliting the explosion step on this surface
        exp_step = pygame.transform.rotate(exp_step, self.an - 90)  # Rotating the image
        
        tank_screen.blit(exp_step, (self.x, self.y))  # Bliting curent step on the main tank_screen
    
    def update(self):
        if self.lft > 0:
            self.move()
            self.draw() 
            self.checkKill()
            self.lft -= 1
        elif self.lft >= -6:
            self.explode()
            self.lft -= 1
        
            

            
