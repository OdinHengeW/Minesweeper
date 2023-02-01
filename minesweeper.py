import random
import pygame, sys
from pygame.locals import *
import ctypes

pygame.init()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
SCRSIZE = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1) #add for mac also

SIZEX = 30
SIZEY = 16
SQZIZE = int((SCRSIZE[1] - (SCRSIZE[1] * 0.1))/SIZEY)
DIFFICULTY = 99
WIDTH = SIZEX * SQZIZE
HEIGHT = SIZEY * SQZIZE
myfont = pygame.font.SysFont("monocraft", 20)
fleg = myfont.render("fleg", 1, (255,255,255))
firstclick = True

def lclick(event):
    x = event.pos[0]//SQZIZE
    y = event.pos[1]//SQZIZE
    
    #print(mines[0])
    show_what(x, y)
    #redraw()
    draw()
    
def draw():    
    cunt = 0
    for i in range(SIZEX):
        for j in range(SIZEY):
            if mines[1][i][j] == 1:
                if mines[0][i][j] == 0:
                    pygame.draw.rect(canvas, (128, 128, 128), (i * SQZIZE, j * SQZIZE, SQZIZE, SQZIZE))
                elif mines[0][i][j] == 9:
                    pygame.draw.rect(canvas, (255, 0, 0), (i * SQZIZE, j * SQZIZE, SQZIZE, SQZIZE))
                    bomb = myfont.render("BOMB", 1, (255,255,255))
                    canvas.blit(bomb, (i * SQZIZE + (SQZIZE/2 - bomb.get_width() / 2), j * SQZIZE + (SQZIZE/2 - bomb.get_height() / 2)))  
                elif 0 < mines[0][i][j] < 9:
                    pygame.draw.rect(canvas, (128, 128, 128), (i * SQZIZE, j * SQZIZE, SQZIZE, SQZIZE))
                    nomber = myfont.render(str(mines[0][i][j]), 1, (255,255,0))
                    canvas.blit(nomber, (i * SQZIZE + (SQZIZE/2 - nomber.get_width() / 2), j * SQZIZE + (SQZIZE/2 - nomber.get_height() / 2)))  
            else:
                
                if mines[0][i][j] != 9:
                    cunt += 1
                
    if cunt == 0:
        win = myfont.render("win. Press enter to reset!", 1, (255,255,255))
        canvas.blit(win, (WIDTH / 2 - win.get_width() / 2, HEIGHT / 2 - win.get_height() / 2))  
    else:
        cunt = 0
    pygame.display.update()
        
def rclick(event):
    
    x = event.pos[0]//SQZIZE
    y = event.pos[1]//SQZIZE
    
    if mines[1][x][y] == 0:
        mines[1][x][y] = 2
        canvas.blit(fleg, (x * SQZIZE + (SQZIZE/2 - fleg.get_width() / 2), y * SQZIZE + (SQZIZE/2 - fleg.get_height() / 2)))  
    elif mines[1][x][y] == 2:
        mines[1][x][y] = 0
        #redrawsq(x, y)
        canvas.fill((0,0,0)) 
        redraw()
        draw()
        for i in range(SIZEX):
            for j in range(SIZEY):
                if mines[1][i][j] == 2:
                    canvas.blit(fleg, (i * SQZIZE + (SQZIZE/2 - fleg.get_width() / 2), j * SQZIZE + (SQZIZE/2 - fleg.get_height() / 2)))  
    pygame.display.update()
        
        
def show_what(x, y):
    uncover = []
    additional = []
    cont = 0
    uncover.append((x, y))
    if mines[1][x][y] != 2:
        if mines[0][x][y] == 0:
            while 1:
                neighbours = get_neighbours(uncover[0][0], uncover[0][1], SIZEX, SIZEY)
                for r, c in neighbours:
                    if mines[1][r][c] != 1 and mines[0][r][c] == 0 and (r, c) not in uncover:
                        uncover.append((r, c))
                for i, j in uncover:
                    for r, c in get_neighbours(i, j, SIZEX, SIZEY):
                        if mines[0][r][c] == 0 and mines[1][r][c] == 0 and (r, c) not in uncover:
                            uncover.append((r, c))
                            cont += 1
                if cont == 0:
                    break
                cont = 0
                #print(uncover)

            for i in uncover:
                neighbours = get_neighbours(i[0], i[1], SIZEX, SIZEY)
                for r, c in neighbours:
                    if 0 < mines[0][r][c] < 9 and mines[1][r][c] != 1 and (r, c) not in uncover:
                        additional.append((r, c))
            for i in additional:
                uncover.append(i)
            while len(uncover) > 0:
                mines[1][uncover[0][0]][uncover[0][1]] = 1
                uncover.pop(0)
        else:
            mines[1][x][y] = 1

def numbers():
    count = 0
    
    for i in range(SIZEX):
        for j in range(SIZEY):
            if mines[0][i][j] != 9:
                neighbours = get_neighbours(i, j, SIZEX, SIZEY)

                for neighbour in neighbours:
                    if mines[0][neighbour[0]][neighbour[1]] == 9:
                        count += 1
                mines[0][i][j] = count
                count = 0
            
def get_neighbours(row, col, rows, cols):
    neighbours = []
    
    if row > 0:
        neighbours.append((row - 1, col))
    if col > 0:
        neighbours.append((row, col - 1))
    if row < rows - 1:
        neighbours.append((row + 1, col))
    if col < cols - 1:
        neighbours.append((row, col + 1))
        
    if row > 0 and col > 0:
        neighbours.append((row - 1, col - 1))
    if row < rows - 1 and col < cols - 1:
        neighbours.append((row + 1, col + 1))
    if row < rows - 1 and col > 0:
        neighbours.append((row + 1, col - 1))
    if row > 0 and col < cols - 1:
        neighbours.append((row - 1, col + 1))
    return neighbours

"""def redrawsq(x, y):
    pygame.draw.rect(canvas, (0, 0, 0), (x * SQZIZE, y * SQZIZE, SQZIZE, SQZIZE))
    pygame.display.update()
"""
def redraw():
    canvas.fill(BLACK)
    for i in range(1, SIZEX):
        pygame.draw.line(canvas, WHITE, [i * WIDTH / SIZEX, 0],[i * WIDTH / SIZEX, HEIGHT], 1)

    for i in range(1, SIZEY):
        pygame.draw.line(canvas, WHITE, [0, i * HEIGHT / SIZEY],[WIDTH, i * HEIGHT / SIZEY], 1)
    #pygame.display.update()
    
def set_mines():
    for i in range(DIFFICULTY):
        minex = random.randint(0, SIZEX - 1)
        miney = random.randint(0, SIZEY - 1)
    
        while mines[0][minex][miney] == 9 or mines[1][minex][miney] == 3:
            minex = random.randint(0, SIZEX - 1)
            miney = random.randint(0, SIZEY - 1)
        mines[0][minex][miney] = 9
    numbers()
    
def reset(event):
    global mines
    global firstclick
    firstclick = True
    #print(event)
    redraw()
    mines = [[[0 for j in range(SIZEY)] for i in range(SIZEX)] for p in range(2)]
    #set_mines()
    draw()

#canvas declaration
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')
redraw()
#minefield
mines = [[[0 for j in range(SIZEY)] for i in range(SIZEX)] for p in range(2)]



#game loop
while True:

    for event in pygame.event.get():

        if event.type == MOUSEBUTTONUP:
            
            if firstclick:
                firstclick = False
                x = event.pos[0]//SQZIZE
                y = event.pos[1]//SQZIZE
                mines[1][x][y] = 3
                
                for i, j in get_neighbours(x, y, SIZEX, SIZEY):
                    mines[1][i][j] = 3
                set_mines()
            if event.button == 1:
                lclick(event)
            elif event.button == 3:
                rclick(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_RETURN:
                reset(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()