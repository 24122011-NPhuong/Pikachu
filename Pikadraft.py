# INSTRUCTION: Just need to change this path and can run game
PATH = './Pikadraft' 

import pygame, sys, random, copy, time, collections, os, json, hashlib
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox


FPS = 10
WINDOWWIDTH = 1000
WINDOWHEIGHT = 570
BOXSIZE = 55
TIMEBAR_LENGTH = 300
TIMEBAR_WIDTH = 30
LEVELMAX = 5
lives = 5
GAMETIME = 240
GETHINTTIME = 20
board_width = 14
board_height = 9
numheroes_onboard = 21
numsameheroes = 4
x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2  
y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# set up the colors
GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BOLDGREEN = (0, 175, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = NAVYBLUE
HIGHLIGHTCOLOR = BLUE
BORDERCOLOR = RED

# TIMEBAR setup
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, y_margin // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN

# Make a dict to store scaled images
LISTHEROES = os.listdir('hero_icon')
NUMHEROES = len(LISTHEROES)
HEROES_DICT = {}

for i in range(len(LISTHEROES)):
    HEROES_DICT[i + 1] = pygame.transform.scale(pygame.image.load('hero_icon/' + LISTHEROES[i]), (BOXSIZE, BOXSIZE))

# Load pictures
aegis = pygame.image.load('aegis_2.jpg')
aegis = pygame.transform.scale(aegis, (45, 45))

# Load background
startBG = pygame.image.load('dota_background/startBG.jpg')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))

listBG = [pygame.image.load('dota_background/{}.jpg'.format(i)) for i in range(15)]
for i in range(len(listBG)):
    listBG[i] = pygame.transform.scale(listBG[i], (WINDOWWIDTH, WINDOWHEIGHT))

# Load sound and music
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('beep4.ogg')
getPointSound = pygame.mixer.Sound('beep1.ogg')
startScreenSound = pygame.mixer.Sound('warriors-of-the-night-assemble.wav')
listMusicBG = ['musicBG1.mp3', 'musicBG2.mp3', 'musicBG3.mp3', 'musicBG4.mp3', 'musicBG5.mp3']

# Load sound effects
LIST_SOUNDEFFECT = os.listdir('sound_effect')

for i in range(len(LIST_SOUNDEFFECT)):
    LIST_SOUNDEFFECT[i] = pygame.mixer.Sound('sound_effect/' + LIST_SOUNDEFFECT[i])


def updateGameVariables(difficulty):
    global board_width, board_height, numheroes_onboard, x_margin, y_margin, lives, numsameheroes
    if difficulty == "easy":
        board_width = 8
        board_height = 8
        numheroes_onboard = 9  
        numsameheroes = 4
        lives = 3
        x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2
        y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2

    elif difficulty == "medium":
        board_width = 10
        board_height = 9
        numheroes_onboard = 28
        numsameheroes = 2
        lives = 5
        x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2
        y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2
        
    elif difficulty == "hard":
        board_width = 14
        board_height = 9
        lives = 7
        numheroes_onboard = 42
        numsameheroes = 2
        x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2
        y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2

def showStartScreen():
    global board_width, board_height, numheroes_onboard, x_margin, y_margin
    default_color = RED
    clicked_color = GRAY

    while True:
        DISPLAYSURF.blit(startBG, (0, 0))

        # Render buttons for each mode
        easySurf = BASICFONT.render('EASY', True, default_color)
        easyRect = easySurf.get_rect()
        easyRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 100)

        mediumSurf = BASICFONT.render('MEDIUM', True, default_color)
        mediumRect = mediumSurf.get_rect()
        mediumRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)

        hardSurf = BASICFONT.render('HARD', True, default_color)
        hardRect = hardSurf.get_rect()
        hardRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 100)

        # Draw buttons on the screen
        DISPLAYSURF.blit(easySurf, easyRect)
        DISPLAYSURF.blit(mediumSurf, mediumRect)
        DISPLAYSURF.blit(hardSurf, hardRect)

        # Draw default borders (red)
        pygame.draw.rect(DISPLAYSURF, default_color, easyRect, 4)
        pygame.draw.rect(DISPLAYSURF, default_color, mediumRect, 4)
        pygame.draw.rect(DISPLAYSURF, default_color, hardRect, 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos

                if easyRect.collidepoint((mousex, mousey)):
                    easySurf = BASICFONT.render('EASY', True, clicked_color)
                    updateGameVariables("easy")  
                    pygame.draw.rect(DISPLAYSURF, clicked_color, easyRect, 4)
                    DISPLAYSURF.blit(easySurf, easyRect)
                    pygame.display.update()
                    pygame.time.wait(500)
                    return  

                elif mediumRect.collidepoint((mousex, mousey)):
                    mediumSurf = BASICFONT.render('MEDIUM', True, clicked_color)
                    updateGameVariables("medium")  
                    pygame.draw.rect(DISPLAYSURF, clicked_color, mediumRect, 4)
                    DISPLAYSURF.blit(mediumSurf, mediumRect)
                    pygame.display.update()
                    pygame.time.wait(500)
                    return  

                elif hardRect.collidepoint((mousex, mousey)):
                    hardSurf = BASICFONT.render('HARD', True, clicked_color)
                    updateGameVariables("hard")  
                    pygame.draw.rect(DISPLAYSURF, clicked_color, hardRect, 4)
                    DISPLAYSURF.blit(hardSurf, hardRect)
                    pygame.display.update()
                    pygame.time.wait(500)
                    return  

        pygame.display.update()
        FPSCLOCK.tick(FPS)
 

def runGame():
    mainBoard = getRandomizedBoard()
    clickedBoxes = [] # stores the (x, y) of clicked boxes
    firstSelection = None # stores the (x, y) of the first box clicked
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)

    global GAMETIME, lives, LEVEL, TIMEBONUS, STARTTIME
    STARTTIME = time.time()
    TIMEBONUS = 0

    randomBG = listBG[LEVEL - 1]
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1, 0.0)
    
    while True:
        mouseClicked = False

        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard, clickedBoxes)
        drawTimeBar()
        drawLives()
        drawLevel()
        # quit_button_rect = drawQuit_btn()

        if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
            LEVEL = LEVELMAX + 1
            return
        if time.time() - lastTimeGetPoint >= GETHINTTIME:
            drawHint(hint)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey == event.pos
                mouseClicked = True
                # if quit_button_rect.collidepoint(mousex, mousey):
                #     pygame.mixer.music.stop()
                #     return showStartScreen() 
                             
            if event.type == KEYUP:
                if event.key == K_n:
                    boxy1, boxx1 = hint[0][0], hint[0][1]
                    boxy2, boxx2 = hint[1][0], hint[1][1]
                    mainBoard[boxy1][boxx1] = 0
                    mainBoard[boxy2][boxx2] = 0
                    TIMEBONUS += 1
                    alterBoardWithLevel(mainBoard, boxy1, boxx1, boxy2, boxx2, LEVEL)

                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard)
                        pygame.display.update()
                        return

                    if not(mainBoard[boxy1][boxx1] != 0 and bfs(mainBoard, boxy1, boxx1, boxy2, boxx2)):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(100)
                            resetBoard(mainBoard)
                            lives += -1
                            if lives == 0:
                                LEVEL = LEVELMAX + 1
                                return

                            hint = getHint(mainBoard)

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0:
            # The mouse is currently over a box
            drawHighlightBox(mainBoard, boxx, boxy)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0 and mouseClicked == True:
            # The mouse is clicking on a box
            clickedBoxes.append((boxx, boxy))
            drawClickedBox(mainBoard, clickedBoxes)
            mouseClicked = False

            if firstSelection == None:
                firstSelection = (boxx, boxy)
                clickSound.play()
            else:
                path = bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx)
                if path:
                    if random.randint(0, 100) < 20:
                        soundObject = random.choice(LIST_SOUNDEFFECT)
                        soundObject.play()
                    getPointSound.play()
                    mainBoard[firstSelection[1]][firstSelection[0]] = 0
                    mainBoard[boxy][boxx] = 0
                    drawPath(mainBoard, path)
                    TIMEBONUS += 1
                    lastTimeGetPoint = time.time()
                    alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, LEVEL)

                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard)
                        pygame.display.update()
                        return
                    if not(mainBoard[hint[0][0]][hint[0][1]] != 0 and bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(500)
                            resetBoard(mainBoard)
                            lives += -1
                            if lives == 0:
                                LEVEL = LEVELMAX + 1
                                return

                            hint = getHint(mainBoard)
                else:
                    clickSound.play()

                clickedBoxes = []
                firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        pygame.mixer.music.stop()
    
def getRandomizedBoard():
    list_pokemons = list(range(1, len(HEROES_DICT) + 1))
    random.shuffle(list_pokemons)
    list_pokemons = list_pokemons[:numheroes_onboard] * numsameheroes
    random.shuffle(list_pokemons)
    board = [[0 for _ in range(board_width)] for _ in range(board_height)]

    # We create a board of images surrounded by 4 arrays of zeroes
    k = 0
    for i in range(1, board_height - 1):
        for j in range(1, board_width - 1):
            board[i][j] = list_pokemons[k]
            k += 1
    return board

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu Classic')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    while True:
        random.shuffle(listBG)
        random.shuffle(listMusicBG)
        LEVEL = 1
        showStartScreen()
        while LEVEL <= LEVELMAX:
            runGame()
            LEVEL += 1
            pygame.time.wait(1000)
        showGameOverScreen()

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + x_margin
    top = boxy * BOXSIZE + y_margin
    return left, top

def getBoxAtPixel(x, y):
    if x <= x_margin or x >= WINDOWWIDTH - x_margin or y <= y_margin or y >= WINDOWHEIGHT - y_margin:
        return None, None
    return (x - x_margin) // BOXSIZE, (y - y_margin) // BOXSIZE

def drawBoard(board):
    for boxx in range(board_width):
        for boxy in range(board_height):
            if board[boxy][boxx] != 0:
                left, top = leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                DISPLAYSURF.blit(HEROES_DICT[board[boxy][boxx]], boxRect)

def drawLevel():
    
    level_font = pygame.font.SysFont('Arial', 25,bold=True)
    level_text = level_font.render(f"LEVEL {LEVEL}/5", True, ORANGE)
    
    DISPLAYSURF.blit(level_text, ((WINDOWWIDTH // 2) - 50 , barPos[1] + 40))
    
def drawHighlightBox(board, boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 2, top - 2,
                                                   BOXSIZE + 4, BOXSIZE + 4), 2)

def drawClickedBox(board, clickedBoxes):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = HEROES_DICT[board[boxy][boxx]].copy()

        # Darken the clicked image
        image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
        DISPLAYSURF.blit(image, boxRect)

def bfs(board, boxy1, boxx1, boxy2, boxx2):
    def backtrace(parent, boxy1, boxx1, boxy2, boxx2):
        start = (boxy1, boxx1, 0, 'no_direction')
        end = 0
        for node in parent:
            if node[:2] == (boxy2, boxx2):
                end = node

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()

        for i in range(len(path)):
            path[i] = path[i][:2]
        return path

    if board[boxy1][boxx1] != board[boxy2][boxx2]:
        return []

    n = len(board)
    m = len(board[0])

    import collections
    q = collections.deque()
    q.append((boxy1, boxx1, 0, 'no_direction'))
    visited = set()
    visited.add((boxy1, boxx1, 0, 'no_direction'))
    parent = {}

    while len(q) > 0:
        r, c, num_turns, direction = q.popleft()
        if (r, c) != (boxy1, boxx1) and (r, c) == (boxy2, boxx2):
            return backtrace(parent, boxy1, boxx1, boxy2, boxx2)

        dict_directions = {(r + 1, c): 'down', (r - 1, c): 'up', (r, c - 1): 'left',
                           (r, c + 1): 'right'}
        for neiborX, neiborY in dict_directions:
            next_direction = dict_directions[(neiborX, neiborY)]
            if 0 <= neiborX <= n - 1 and 0 <= neiborY <= m - 1 and (
                    board[neiborX][neiborY] == 0 or (neiborX, neiborY) == (boxy2, boxx2)):
                if direction == 'no_direction':
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction == next_direction and (
                        neiborX, neiborY, num_turns, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction != next_direction and num_turns < 2 and (
                        neiborX, neiborY, num_turns + 1, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns + 1, next_direction))
                    visited.add((neiborX, neiborY, num_turns + 1, next_direction))
                    parent[
                        (neiborX, neiborY, num_turns + 1, next_direction)] = (
                    r, c, num_turns, direction)
    return []

def getCenterPos(pos): # pos is coordinate of a box in mainBoard
    left, top = leftTopCoordsOfBox(pos[1], pos[0])
    return tuple([left + BOXSIZE // 2, top + BOXSIZE // 2])

def drawPath(board, path):
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i + 1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos, 4)
    pygame.display.update()
    pygame.time.wait(300)

def drawTimeBar():
    progress = 1 - ((time.time() - STARTTIME - TIMEBONUS) / GAMETIME)

    pygame.draw.rect(DISPLAYSURF, borderColor, (barPos, barSize), 1)
    innerPos = (barPos[0] + 2, barPos[1] + 2)
    innerSize = ((barSize[0] - 4) * progress, barSize[1] - 4)
    pygame.draw.rect(DISPLAYSURF, barColor, (innerPos, innerSize))

def showGameOverScreen():
    playAgainFont = pygame.font.Font('freesansbold.ttf', 50)
    playAgainSurf = playAgainFont.render('Play Again?', True, PURPLE)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(playAgainSurf, playAgainRect)
    pygame.draw.rect(DISPLAYSURF, PURPLE, playAgainRect, 4)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if playAgainRect.collidepoint((mousex, mousey)):
                    return

def getHint(board):
    boxPokesLocated = collections.defaultdict(list)
    hint = []
    for boxy in range(board_height):
        for boxx in range(board_width):
            if board[boxy][boxx] != 0:
                boxPokesLocated[board[boxy][boxx]].append((boxy, boxx))
    for boxy in range(board_height):
        for boxx in range(board_width):
            if board[boxy][boxx] != 0:
                for otherBox in boxPokesLocated[board[boxy][boxx]]:
                    if otherBox != (boxy, boxx) and bfs(board, boxy, boxx, otherBox[0], otherBox[1]):
                        hint.append((boxy, boxx))
                        hint.append(otherBox)
                        return hint
    return []

def drawHint(hint):
    for boxy, boxx in hint:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top,
                                                       BOXSIZE, BOXSIZE), 2)

def resetBoard(board):
    pokesOnBoard = []
    for boxy in range(board_height):
        for boxx in range(board_width):
            if board[boxy][boxx] != 0:
                pokesOnBoard.append(board[boxy][boxx])
    referencedList = pokesOnBoard[:]
    while referencedList == pokesOnBoard:
        random.shuffle(pokesOnBoard)

    i = 0
    for boxy in range(board_height):
        for boxx in range(board_width):
            if board[boxy][boxx] != 0:
                board[boxy][boxx] = pokesOnBoard[i]
                i += 1
    return board

def isGameComplete(board):
    for boxy in range(board_height):
        for boxx in range(board_width):
            if board[boxy][boxx] != 0:
                return False
    return True

def alterBoardWithLevel(board, boxy1, boxx1, boxy2, boxx2, level):

    # Level 2: All the pokemons move up to the top boundary
    if level == 2:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(board_height):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            while len(cur_list) < board_height:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 3: All the pokemons move down to the bottom boundary
    if level == 3:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(board_height):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            cur_list.append(0)
            cur_list = [0] * (board_height - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 4: All the pokemons move left to the left boundary
    if level == 4:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(board_width):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            while len(cur_list) < board_width:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    # Level 5: All the pokemons move right to the right boundary
    if level == 5:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(board_width):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            cur_list.append(0)
            cur_list = [0] * (board_width - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    return board

def drawLives():
    aegisRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
    DISPLAYSURF.blit(aegis, aegisRect)
    livesSurf = LIVESFONT.render(str(lives), True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)

if __name__ == '__main__':
    main()



