from random import randint


class Cell:
    def __init__(self, state, right=0, bottom=0, color=0):
        self.st = state
        self.right = right
        self.bottom = bottom 


def copyline(prevline):
    newline = []
    for pc in prevline:
        newcell = Cell(pc.st, pc.right, pc.bottom)
        newline.append(newcell)
    return newline
    
def genline(prevline, w, last = 0):

    line = copyline(prevline)
    
    if last: #generating last line
        for i in range(len(line) - 1):
            line[i].bottom = 1
            line[i].right = 0
        line[i + 1].bottom = 1
        return line[::]
    
    used = set()
    
    for cell in line:  # Preparing the line for the next generation
        cell.right = 0
        if cell.bottom:
            cell.st = 0
        used.add(cell.st)
        cell.bottom = 0   
    if 0 in used: used.remove(0)
    for cell in line:
        if not cell.st:
            cell.st = max(used) + 1
            used.add(cell.st)
       
    for i in range(len(line)):
        #generating RIGHT border
        if i < len(line) - 1:
            if randint(0, 1):
                if line[i].st != line[i + 1].st:
                    line[i].right = 1   
            elif line[i].st == line[i + 1].st:
                line[i].right = 1
            else:
                line[i + 1].st = line[i].st   
        else:
            line[i].right = 1
        
        #generating BOTTOM border
        if randint(0, 1):
            cnt = 0
            for j in line:
                if j.st == line[i].st and j.bottom == 0:
                    cnt += 1
            if cnt > 1:
                line[i].bottom = True

    return copyline(line)


def maze_gen(w, h):
    prevline = [Cell(i + 11) for i in range(w)]
    
    maze = [[Cell(-1, 1, 1, 0) for i in range(w + 2)]]
    
    for i in range(h):
        if i == h - 1:
            line = genline(prevline, w, 1)
        else:
            line = genline(prevline, w)
        newline = [Cell(-1, 1, 1, 0)] + line + [Cell(-1, 1, 1, 0)]
        maze.append(newline)
        prevline = copyline(line)
    
    maze.append([Cell(-1, 1, 1, 0) for i in range(w + 2)])   
    return maze