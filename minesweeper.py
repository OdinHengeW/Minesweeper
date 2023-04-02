import random
import pygame, sys
import time

pygame.init()

#globals
#colours
SCRSIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h - 100)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
YELLOW = (255,255,0)
RED = (255,0,0)

#Game parameters
SIZEX = 30
SIZEY = 16
DIFFICULTY = 99

#window size
RATIO = SIZEX / SIZEY
TIMERHEIGHT = int(SCRSIZE[1] / 20)
WIDTH = SCRSIZE[0]
HEIGHT = int(SIZEY * (WIDTH // SIZEX))
TOTHEIGHT = HEIGHT + TIMERHEIGHT
SQSIZE = WIDTH // SIZEX 

#fonts
FONT = pygame.font.SysFont("Arial", int(2 * SQSIZE / 3)) 
TIMEFONT = pygame.font.SysFont("Arial", int(TIMERHEIGHT))
  
#status of game
firstclick = True
gameover = False
won = False

#Reveals squares that should be shown when left clicking
def lclick(event):
    try:
        x = event.pos[0]//SQSIZE
        y = int((event.pos[1] - TIMERHEIGHT)//SQSIZE)
    except:
        x = pygame.mouse.get_pos()[0]//SQSIZE
        y = int((pygame.mouse.get_pos()[1] - TIMERHEIGHT)//SQSIZE)
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
            show_what(x, y)
        draw()
#Draws squares on board based on their value in "mines"
def draw():    
    global won
    global gameover
    bombcount = 0
    for i in range(SIZEX):
        for j in range(SIZEY):
            if mines[1][i][j] == 1:
                if mines[0][i][j] == 0:
                    canvas.fill(GRAY, (i * SQSIZE, j * SQSIZE + TIMERHEIGHT, SQSIZE, SQSIZE))
                elif 0 < mines[0][i][j] < 9:
                    canvas.fill(GRAY, (i * SQSIZE, j * SQSIZE + TIMERHEIGHT, SQSIZE, SQSIZE))
                    nomber = FONT.render(str(mines[0][i][j]), 1, YELLOW)
                    canvas.blit(nomber, (i * SQSIZE + (SQSIZE/2 - nomber.get_width() / 2), j * SQSIZE + (SQSIZE/2 - nomber.get_height() / 2) + TIMERHEIGHT))  
                elif mines[0][i][j] == 9:
                    canvas.fill(RED, (i * SQSIZE, j * SQSIZE + TIMERHEIGHT, SQSIZE, SQSIZE))
                    bomb = FONT.render("¤", 1, (255,255,255))
                    canvas.blit(bomb, (i * SQSIZE + (SQSIZE/2 - bomb.get_width() / 2), j * SQSIZE + (SQSIZE/2 - bomb.get_height() / 2) + TIMERHEIGHT)) 
                    gameover = True 
            else:   
                if mines[0][i][j] != 9:
                    bombcount += 1
                if mines[1][i][j] == 2:
                    flag = FONT.render("F", 1, WHITE)
                    canvas.blit(flag, (i * SQSIZE + (SQSIZE/2 - flag.get_width() / 2), j * SQSIZE + (SQSIZE/2 - flag.get_height() / 2) + TIMERHEIGHT))  
    if bombcount == 0:
        win = FONT.render("You won! Press enter to reset!", 1, WHITE)
        canvas.blit(win, (WIDTH / 2 - win.get_width() / 2, HEIGHT / 2 - win.get_height() / 2))
        won = True
    else:
        bombcount = 0
    if gameover:
        lose = FONT.render("You lost! Press enter to reset!", 1, WHITE)
        canvas.blit(lose, (WIDTH / 2 - lose.get_width() / 2, HEIGHT / 2 - lose.get_height() / 2))
        return
    pygame.display.update()
  
#Places and removes flags      
def rclick(event):
    global gameover
    global won
    if not gameover and not won:    
        try:
            x = event.pos[0]//SQSIZE
            y = int((event.pos[1] - TIMERHEIGHT)//SQSIZE)
        except:
            x = pygame.mouse.get_pos()[0]//SQSIZE
            y = int((pygame.mouse.get_pos()[1] - TIMERHEIGHT)//SQSIZE)
        if y >= 0:
            if mines[1][x][y] == 0:
                mines[1][x][y] = 2
                flag = FONT.render("F", 1, WHITE)
                canvas.blit(flag, (x * SQSIZE + (SQSIZE/2 - flag.get_width() / 2), y * SQSIZE + (SQSIZE/2 - flag.get_height() / 2) + TIMERHEIGHT))  
            elif mines[1][x][y] == 2:
                canvas.fill(BLACK, (x * SQSIZE + 1, y * SQSIZE + 1 + TIMERHEIGHT, SQSIZE - 1, SQSIZE - 1))
                mines[1][x][y] = 0
        pygame.display.update()
        
#Fetches the squares that should be visible after a left click
def show_what(x, y):
    uncover = []
    if mines[1][x][y] != 2:
        uncover.append((x, y)) 
        if mines[0][x][y] == 0 and mines[1][x][y] != 1:
            mines[1][x][y] = 1
            neigbours = get_neighbours(x, y, SIZEX, SIZEY)
            while 1:
                for r, c in neigbours:
                    if mines[0][r][c] < 9 and mines[1][r][c] != 1:
                        mines[1][r][c] = 1
                        if mines[0][r][c] == 0:
                            uncover.append((r, c))
                if len(uncover) > 0:       
                    neigbours = get_neighbours(uncover[0][0], uncover[0][1], SIZEX, SIZEY)
                    uncover.pop(0)
                else:
                    break
        else:
            mines[1][x][y] = 1

#Gives squares with neighbouring bombs a value in "mines" that represents the number of bombs around it.
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
       
#Gets the neighbours of a given square     
def get_neighbours(row, col, rows, cols):
    neighbours = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= (row + i) < rows and 0 <= (col + j) < cols: 
                if not (i == 0 and j == 0):
                    neighbours.append((row + i, col + j))
    return neighbours

#Redraws the grid lines on the screen
def redraw():
    canvas.fill(BLACK)
    for i in range(1, SIZEX):
        pygame.draw.line(canvas, WHITE, [i * WIDTH / SIZEX, TIMERHEIGHT],[i * WIDTH / SIZEX, TOTHEIGHT], 1)

    for i in range(SIZEY):
        pygame.draw.line(canvas, WHITE, [0, (i * HEIGHT / SIZEY) + TIMERHEIGHT],[WIDTH, (i * HEIGHT / SIZEY) + TIMERHEIGHT], 1)

#Randomly places mines 
def set_mines():
    for i in range(DIFFICULTY):
        minex = random.randint(0, SIZEX - 1)
        miney = random.randint(0, SIZEY - 1)
        while mines[0][minex][miney] == 9 or mines[0][minex][miney] == 10:
            minex = random.randint(0, SIZEX - 1)
            miney = random.randint(0, SIZEY - 1)
        mines[0][minex][miney] = 9
    numbers()
    
#Resets globals and other variables
def reset():
    global mines
    global timer
    global firstclick
    global won
    global gameover
    firstclick = True
    gameover = False
    won = False
    redraw()
    mines = [[[0 for j in range(SIZEY)] for i in range(SIZEX)] for p in range(2)]
    draw()
    timer = TIMEFONT.render(str(0), 1, WHITE)
    canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))

#Recalculates the globals based on the new size of the window.
def redo_globals():
    global FONT 
    global canvas
    global RATIO
    global SQSIZE
    global WIDTH
    global HEIGHT
    global TOTHEIGHT
    
    new_width = canvas.get_width()
    new_height = canvas.get_height()
    if new_width != WIDTH:
        SQSIZE = int(new_width / SIZEX)
        WIDTH = int(SQSIZE * SIZEX)
        HEIGHT = int(WIDTH / RATIO)
    elif new_height != HEIGHT:
        SQSIZE = int(new_height / SIZEY)
        HEIGHT = int(SQSIZE * SIZEY)
        WIDTH = int(HEIGHT * RATIO)
    TOTHEIGHT = TIMERHEIGHT + HEIGHT
    
    FONT = pygame.font.SysFont("Arial", int(2 * SQSIZE / 3))
    canvas = pygame.display.set_mode((WIDTH, TOTHEIGHT), pygame.RESIZABLE)

#canvas declaration    
canvas = pygame.display.set_mode((WIDTH, TOTHEIGHT), pygame.RESIZABLE)

#wondow setup
pygame.display.set_caption('Minesweeper')
redraw()
timer = TIMEFONT.render(str(0), 1, WHITE)
canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))

#initializing clock object
clock = pygame.time.Clock()

#minefield
mines = [[[0 for j in range(SIZEY)] for i in range(SIZEX)] for p in range(2)]

#timer variables
dt = 0
lastdt = 0

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            redo_globals()
            redraw()
            draw()
            canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))
        if not gameover and not won:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if firstclick:
                        firstclick = False
                        x = event.pos[0]//SQSIZE
                        y = int((event.pos[1] - TIMERHEIGHT)//SQSIZE)
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
            elif event.key == pygame.K_LALT:
                if not firstclick and not gameover and not won:
                    lclick(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not firstclick and not gameover and not won:
        lastdt = dt
        dt = int(time.time() - starttime) + 1
        if lastdt != dt:
            timer = TIMEFONT.render(str(dt), 1, WHITE)
            canvas.fill((0, 0, 0), ((WIDTH/2) - (timer.get_width()/2) - 30, (TIMERHEIGHT/2) - (timer.get_height()/2), timer.get_width() + 30, TIMERHEIGHT))
            canvas.blit(timer, ((WIDTH/2) - (timer.get_width()/2), (TIMERHEIGHT/2) - (timer.get_height()/2)))
    pygame.display.update()
    clock.tick(60)