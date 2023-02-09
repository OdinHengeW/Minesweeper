import random
import pygame, sys
import ctypes
import time

pygame.init()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
try:
    SCRSIZE = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1) #add for mac also
except:
    SCRSIZE = (1400, 860)
SIZEX = 30
SIZEY = 16
DIFFICULTY = 99
SQZIZE = int((SCRSIZE[1] - (SCRSIZE[1] * 0.1))/SIZEY) 
TIMERHEIGHT = SCRSIZE[1] / 20
WIDTH = SIZEX * SQZIZE
HEIGHT = SIZEY * SQZIZE 
TOTHEIGHT = HEIGHT + TIMERHEIGHT
try:
    myfont = pygame.font.Font(r"C:\Users\Anders\AppData\Local\Microsoft\Windows\Fonts\Monocraft.otf", int(SQZIZE / 2)) #only works on this pc
    timefont = pygame.font.Font(r"C:\Users\Anders\AppData\Local\Microsoft\Windows\Fonts\Monocraft.otf", int(TIMERHEIGHT))
except:
    myfont = pygame.font.SysFont("Monocraft", int(SQZIZE / 2)) 
    timefont = pygame.font.SysFont("Monocraft", int(TIMERHEIGHT))
    
fleg = myfont.render("F", 1, (255,255,255))
firstclick = True
gameover = False
won = False

def lclick(event):
    x = event.pos[0]//SQZIZE
    y = int((event.pos[1] - TIMERHEIGHT)//SQZIZE)

    #clicking a number tile reveals surrounding tiles if there is a sufficient amount of flags around the number tile
    if y >= 0:
        if 0 < mines[0][x][y] < 9 and mines[1][x][y] == 1:
            bordering_flags = 0
            neighbours = get_neighbours(x, y, SIZEX, SIZEY)
            for r, c in neighbours:
                if mines[1][r][c] == 2:
                    bordering_flags += 1
            if bordering_flags == mines[0][x][y]:
                for r, c in neighbours:
                    if mines[1][r][c] != 2:
                        if mines[0][r][c] == 0:
                            show_what(r,c)
                        else:
                            mines[1][r][c] = 1
        else:
            #print(mines[0])
            show_what(x, y)
            #redraw()
        draw()

def draw():    
    global won
    global gameover
    bombcount = 0
    for i in range(SIZEX):
        for j in range(SIZEY):
            if mines[1][i][j] == 1:
                if mines[0][i][j] == 0:
                    pygame.Rect.move
                    canvas.fill((128, 128, 128), (i * SQZIZE, j * SQZIZE + TIMERHEIGHT, SQZIZE, SQZIZE))
                    #pygame.draw.rect(canvas, (128, 128, 128), (i * SQZIZE, j * SQZIZE + TIMERHEIGHT, SQZIZE, SQZIZE))
                elif 0 < mines[0][i][j] < 9:
                    canvas.fill((128, 128, 128), (i * SQZIZE, j * SQZIZE + TIMERHEIGHT, SQZIZE, SQZIZE))
                    #pygame.draw.rect(canvas, (128, 128, 128), (i * SQZIZE, j * SQZIZE + TIMERHEIGHT, SQZIZE, SQZIZE))
                    nomber = myfont.render(str(mines[0][i][j]), 1, (255,255,0))
                    canvas.blit(nomber, (i * SQZIZE + (SQZIZE/2 - nomber.get_width() / 2), j * SQZIZE + (SQZIZE/2 - nomber.get_height() / 2) + TIMERHEIGHT))  
                elif mines[0][i][j] == 9:
                    canvas.fill((255, 0, 0), (i * SQZIZE, j * SQZIZE + TIMERHEIGHT, SQZIZE, SQZIZE))
                    # pygame.draw.rect(canvas, (255, 0, 0), (i * SQZIZE, j * SQZIZE + TIMERHEIGHT, SQZIZE, SQZIZE))
                    bomb = myfont.render("¤", 1, (255,255,255))
                    canvas.blit(bomb, (i * SQZIZE + (SQZIZE/2 - bomb.get_width() / 2), j * SQZIZE + (SQZIZE/2 - bomb.get_height() / 2) + TIMERHEIGHT)) 
                    gameover = True        
            else:   
                if mines[0][i][j] != 9:
                    bombcount += 1
    if bombcount == 0:
        win = myfont.render("win. Press enter to reset!", 1, (255,255,255))
        canvas.blit(win, (WIDTH / 2 - win.get_width() / 2, HEIGHT / 2 - win.get_height() / 2))
        won = True  
    else:
        bombcount = 0
    if gameover:
        lose = myfont.render("boom yo ass dead. Press enter to reset!", 1, (255,255,255))
        canvas.blit(lose, (WIDTH / 2 - lose.get_width() / 2, HEIGHT / 2 - lose.get_height() / 2))
        return
    pygame.display.update()
        
def rclick(event):
    try:
        x = event.pos[0]//SQZIZE
        y = int((event.pos[1] - TIMERHEIGHT)//SQZIZE)
    except:
        x = pygame.mouse.get_pos()[0]//SQZIZE
        y = int((pygame.mouse.get_pos()[1] - TIMERHEIGHT)//SQZIZE)
    if y >= 0:
        if mines[1][x][y] == 0:
            mines[1][x][y] = 2
            canvas.blit(fleg, (x * SQZIZE + (SQZIZE/2 - fleg.get_width() / 2), y * SQZIZE + (SQZIZE/2 - fleg.get_height() / 2) + TIMERHEIGHT))  
        elif mines[1][x][y] == 2:
            redrawsq(x, y)
            mines[1][x][y] = 0
        """for i in range(SIZEX):
            for j in range(SIZEY):
                if mines[1][i][j] == 2:
                    canvas.blit(fleg, (i * SQZIZE + (SQZIZE/2 - fleg.get_width() / 2), j * SQZIZE + (SQZIZE/2 - fleg.get_height() / 2) + TIMERHEIGHT))  
    """
    pygame.display.update()
        
def show_what(x, y):
    uncover = []

    
    
    #ändra status på klickad ruta
        #while
            #grannar till rutan
                #om noll
                    #visa
                    #lägg till i lista för att kolla dess grannar
            #ny huvudruta
            #ta bort ny huvudruta från lista
    if mines[1][x][y] != 2:
        uncover.append((x, y)) # nånting funkar inte, kan trycka på flagga o starta skiten, kanske är i set_mines()
        if mines[0][x][y] == 0 and mines[1][x][y] != 1:
            mines[1][x][y] = 1
            neigbours = get_neighbours(x, y, SIZEX, SIZEY)
        
            while 1:
                #mines[1][uncover[0][0]][uncover[0][1]] = 1
                for r, c in neigbours:
                    if mines[0][r][c] < 9 and mines[1][r][c] != 1:
                        mines[1][r][c] = 1
                        if mines[0][r][c] == 0:
                            uncover.append((r, c))
                             
                if len(uncover) > 0: # cont != 0:        
                    neigbours = get_neighbours(uncover[0][0], uncover[0][1], SIZEX, SIZEY)
                    uncover.pop(0)

                else:
                    print("b")
                    break
        else:
            mines[1][x][y] = 1
    
    ## checks all the empty tiles around the pressed tile
    #if mines[1][x][y] != 2:
    #    if mines[0][x][y] == 0:
    #        while 1:
    #            neighbours = get_neighbours(uncover[0][0], uncover[0][1], SIZEX, SIZEY)
    #            for r, c in neighbours:
    #                if mines[1][r][c] != 1 and mines[0][r][c] == 0 and (r, c) not in uncover:
    #                    uncover.append((r, c))
    #            for i, j in uncover:
    #                for r, c in get_neighbours(i, j, SIZEX, SIZEY):
    #                    if mines[0][r][c] == 0 and mines[1][r][c] == 0 and (r, c) not in uncover:
    #                        uncover.append((r, c))
    #                        cont += 1
    #            if cont == 0:
    #                break
    #            cont = 0
    #            #print(uncover)
#
    #        #adds all the number tiles that lie against an empty tile
    #        for i in uncover:
    #            neighbours = get_neighbours(i[0], i[1], SIZEX, SIZEY)
    #            for r, c in neighbours:
    #                if 0 < mines[0][r][c] < 9 and mines[1][r][c] != 1 and (r, c) not in uncover:
    #                    additional.append((r, c))
    #        
    #        #adds all the number tiles to the list of empty tiles
    #        for i in additional:
    #            uncover.append(i)
    #        
    #        #changes status of all tiles in uncover list such that they are to be shown 
    #        while len(uncover) > 0:
    #            mines[1][uncover[0][0]][uncover[0][1]] = 1
    #            uncover.pop(0)
    #    else:
    #        mines[1][x][y] = 1

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
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= (row + i) < rows and 0 <= (col + j) < cols: 
                if not (i == 0 and j == 0):
                    neighbours.append((row + i, col + j))
    return neighbours

def redrawsq(x, y):
    if mines[1][x][y] == 2:
        canvas.fill((0, 0, 0), (x * SQZIZE + 1, y * SQZIZE + 1 + TIMERHEIGHT, SQZIZE - 1, SQZIZE - 1))
    else:
        canvas.fill((128,128,128), (x * SQZIZE + 1, y * SQZIZE + 1 + TIMERHEIGHT, SQZIZE - 1, SQZIZE - 1))
    #pygame.draw.rect(canvas, (0, 0, 0), (x * SQZIZE + 1, y * SQZIZE + 1 + TIMERHEIGHT, SQZIZE - 1, SQZIZE - 1))
    #pygame.display.update()

def redraw():
    canvas.fill(BLACK)
    for i in range(1, SIZEX):
        pygame.draw.line(canvas, WHITE, [i * WIDTH / SIZEX, TIMERHEIGHT],[i * WIDTH / SIZEX, TOTHEIGHT], 1)

    for i in range(SIZEY):
        pygame.draw.line(canvas, WHITE, [0, (i * HEIGHT / SIZEY) + TIMERHEIGHT],[WIDTH, (i * HEIGHT / SIZEY) + TIMERHEIGHT], 1)
    #pygame.display.update()
    
def set_mines():
    for i in range(DIFFICULTY):
        minex = random.randint(0, SIZEX - 1)
        miney = random.randint(0, SIZEY - 1)
        while mines[0][minex][miney] == 9 or mines[0][minex][miney] == 10:
            minex = random.randint(0, SIZEX - 1)
            miney = random.randint(0, SIZEY - 1)
        mines[0][minex][miney] = 9
    numbers()
    
def reset():
    global mines
    global firstclick
    global won
    global gameover
    firstclick = True
    gameover = False
    won = False
    #print(event)
    redraw()
    mines = [[[0 for j in range(SIZEY)] for i in range(SIZEX)] for p in range(2)]
    #set_mines()
    draw()
    timer = timefont.render(str(0), 1, (255,255,255))
    canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))

#canvas declaration
canvas = pygame.display.set_mode((WIDTH, TOTHEIGHT))
pygame.display.set_caption('Minesweeper')
redraw()
timer = timefont.render(str(0), 1, (255,255,255))
canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))

#minefield
mines = [[[0 for j in range(SIZEY)] for i in range(SIZEX)] for p in range(2)]

#timer variables
dt = 0
lastdt = 0

#game loop
while True:
    for event in pygame.event.get():
        if not gameover and not won:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if firstclick:
                        firstclick = False
                        x = event.pos[0]//SQZIZE
                        y = int((event.pos[1] - TIMERHEIGHT)//SQZIZE)
                        if y >= 0:
                            mines[0][x][y] = 10
                            for i, j in get_neighbours(x, y, SIZEX, SIZEY):
                                mines[0][i][j] = 10
                            set_mines()
                            starttime = time.time()
                    lclick(event)
                elif event.button == 3:
                    rclick(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset()
            elif event.key == pygame.K_SPACE:
                rclick(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not firstclick and not gameover and not won:
        lastdt = dt
        dt = int(time.time() - starttime) + 1
        if lastdt != dt:
            timer = timefont.render(str(dt), 1, (255,255,255))
            canvas.fill((0, 0, 0), ((WIDTH/2) - (timer.get_width()/2) - 30, (TIMERHEIGHT/2) - (timer.get_height()/2), timer.get_width() + 30, timer.get_height()))
            # pygame.draw.rect(canvas, (0, 0, 0), ((WIDTH/2) - (timer.get_width()/2) - 30, (TIMERHEIGHT/2) - (timer.get_height()/2), timer.get_width() + 30, timer.get_height()))
            canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))
    pygame.display.update()
    time.sleep(1/60)