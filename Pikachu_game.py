
PATH = './Pikachu_draft' 

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
LISTPOKEMONS = os.listdir('pokemon_icon')
NUMPOKEMONS = len(LISTPOKEMONS)
POKEMONS_DICT = {}

for i in range(len(LISTPOKEMONS)):
    POKEMONS_DICT[i + 1] = pygame.transform.scale(pygame.image.load('pokemon_icon/' + LISTPOKEMONS[i]), (BOXSIZE, BOXSIZE))

# Load pictures
pic = pygame.image.load('pic.png')
pic = pygame.transform.scale(pic, (45, 45))

# Load background
startBG = pygame.image.load('pikachu_background/startBG.jpg')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))

listBG = [pygame.image.load('pikachu_background/{}.jpg'.format(i)) for i in range(15)]
for i in range(len(listBG)):
    listBG[i] = pygame.transform.scale(listBG[i], (WINDOWWIDTH, WINDOWHEIGHT))

# Load sound and music
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('beep4.ogg')
getPointSound = pygame.mixer.Sound('beep1.ogg')
startScreenSound = pygame.mixer.Sound('1-20. Pokémon Gym.mp3')



USER_INFO_FILE = "user_info.json"
GAME_STATE_FILE = "game_state.json"

def initialize_user_info_file():
    try:
        with open(USER_INFO_FILE, "r") as file:
            json.load(file)
    except FileNotFoundError:
        with open(USER_INFO_FILE, "w") as file:
            json.dump({}, file)

def save_user_data(username, password):
    try:
        with open(USER_INFO_FILE, "r") as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    if username in user_data:
        messagebox.showerror("Error", "The username already exists.")
        return False

    user_data[username] = {
        "password": password,
        "game_info": {
            "easy": {"level": 1, "lives": 3},
            "medium": {"level": 1, "lives": 5},
            "hard": {"level": 1, "lives": 7},
        },
    }

    with open(USER_INFO_FILE, "w") as file:
        json.dump(user_data, file)
    return True

def authenticate(username, password):
    try:
        with open(USER_INFO_FILE, "r") as file:
            user_data = json.load(file)
        if username in user_data and user_data[username]["password"] == password:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def register_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if save_user_data(username, password):
            messagebox.showinfo("Success", "Account registered successfully!")
            start_screen(root)

    tk.Label(root, text="Register", font=("Arial", 20)).pack(pady=10)

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Create Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Label(root, text="Confirm Password:").pack(pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=5)

    tk.Button(root, text="Register", command=register).pack(pady=10)
    tk.Button(root, text="Back", command=lambda: login_window(root)).pack(pady=5)
    
def login_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    def login():
        nonlocal username_entry, password_entry

        username = username_entry.get()
        password = password_entry.get()

        if authenticate(username, password):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            root.destroy()
            main(play_type="login", user=username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Label(root, text="Login", font=("Arial", 20)).pack(pady=10)

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Register", command=lambda: register_window(root)).pack(pady=5)
    tk.Button(root, text="Back", command=lambda: start_screen(root)).pack(pady=5)

def start_screen(root=None):
    if root is None:
        root = tk.Tk()
        root.geometry("1000x570")
        root.resizable(False, False)
    else:
        for widget in root.winfo_children():
            widget.destroy()

    root.title("Pikachu Classic")

    tk.Label(root, text="Welcome", font=("Arial", 20)).pack(pady=20)

    def play_as_guest():
        root.destroy()
        main(play_type="guest", user=None)

    tk.Button(root, text="Play as Guest", command=play_as_guest).pack(pady=10)
    tk.Button(root, text="Login to Play", command=lambda: login_window(root)).pack(pady=10)

    root.mainloop()

def updateGameVariables(game_mode):
    global board_width, board_height, numheroes_onboard, x_margin, y_margin, lives, lvl, numsameheroes, player_type, user_acc
        
    if game_mode == "easy":
        board_width = 8
        board_height = 8
        numheroes_onboard = 9  
        numsameheroes = 4
        mode = load_game_state(difficulty)
        lvl = mode['level']
        lives = mode['lives']
        x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2
        y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2

    elif game_mode == "medium":
        board_width = 10
        board_height = 9
        numheroes_onboard = 28
        numsameheroes = 2
        mode = load_game_state(difficulty)
        lvl = int(mode['level'])
        lives = int(mode['lives'])
        x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2
        y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2
        
    elif game_mode == "hard":
        board_width = 14
        board_height = 9
        numheroes_onboard = 42
        numsameheroes = 2
        mode = load_game_state(difficulty)
        lvl = mode['level']
        lives = mode['lives']
        x_margin = (WINDOWWIDTH - (BOXSIZE * board_width)) // 2
        y_margin = (WINDOWHEIGHT - (BOXSIZE * board_height)) // 2

def showMenu_Screen():
    global board_width, board_height, numheroes_onboard, x_margin, y_margin, difficulty
    startScreenSound.play()
    
    while True:
        DISPLAYSURF.blit(startBG, (0, 0))
        
        easy_btnSurf = pygame.image.load('./button_image/easybtn.PNG')
        easy_btnSurf = pygame.transform.scale(easy_btnSurf, (100, 50))
        easy_btnRect = easy_btnSurf.get_rect()
        easy_btnRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 100)

        medium_btnSurf = pygame.image.load('./button_image/normalbtn.PNG')
        medium_btnSurf = pygame.transform.scale(medium_btnSurf, (100, 50))
        medium_btnRect = medium_btnSurf.get_rect()
        medium_btnRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 150)

        hard_btnSurf = pygame.image.load('./button_image/hardbtn.PNG')
        hard_btnSurf = pygame.transform.scale(hard_btnSurf, (100, 50))
        hard_btnRect = hard_btnSurf.get_rect()
        hard_btnRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 200)

        DISPLAYSURF.blit(easy_btnSurf, easy_btnRect)
        DISPLAYSURF.blit(medium_btnSurf, medium_btnRect)
        DISPLAYSURF.blit(hard_btnSurf, hard_btnRect)

        for event in pygame.event.get():
                    if event.type == QUIT:
                        reset_guest_game_state("game_state.json")
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos

                        if easy_btnRect.collidepoint((mousex, mousey)):
                            easy_btnSurf.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
                            difficulty = 'easy'
                            updateGameVariables(difficulty) 
                            DISPLAYSURF.blit(easy_btnSurf, easy_btnRect)
                            startScreenSound.stop()
                            pygame.display.update()
                            pygame.time.wait(500)
                            return 

                        elif medium_btnRect.collidepoint((mousex, mousey)):
                            medium_btnSurf.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
                            difficulty = 'medium'
                            updateGameVariables(difficulty) 
                            DISPLAYSURF.blit(medium_btnSurf, medium_btnRect)
                            startScreenSound.stop()
                            pygame.display.update()
                            pygame.time.wait(500)
                            return 

                        elif hard_btnRect.collidepoint((mousex, mousey)):
                            hard_btnSurf.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
                            difficulty = 'hard'
                            updateGameVariables(difficulty) 
                            DISPLAYSURF.blit(hard_btnSurf, hard_btnRect)
                            startScreenSound.stop()
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

    global GAMETIME, lives, game_lv, TIMEBONUS, STARTTIME
    STARTTIME = time.time()
    TIMEBONUS = 0

    randomBG = listBG[game_lv - 1]
    # randomMusicBG = listMusicBG[game_lv - 1]
    # pygame.mixer.music.load(randomMusicBG)
    # pygame.mixer.music.play(-1, 0.0)
    
    while True:
        mouseClicked = False

        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard, clickedBoxes)
        drawTimeBar()
        drawLives()
        drawLevel()
        exit_to_menu = pygame.image.load('./button_image/exit.png').convert_alpha()
        exit_to_menuRect = draw_image_button(exit_to_menu, 900, 10, 0.15)
        

        if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
            game_lv = LEVELMAX + 1
            return
        if time.time() - lastTimeGetPoint >= GETHINTTIME:
            drawHint(hint)

        for event in pygame.event.get():
            if event.type == QUIT:
                reset_guest_game_state("game_state.json")
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                if exit_to_menuRect.collidepoint((mousex,mousey)):
                    exit_to_menu.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
                    draw_image_button(exit_to_menu, 900, 10, 0.15)
                    save_game_state(difficulty, game_lv, lives, file_in)
                    pygame.display.update()
                    pygame.time.wait(100)
                    return main(player_type, user_acc)
                
            if event.type == KEYUP:
                if event.key == K_n:
                    boxy1, boxx1 = hint[0][0], hint[0][1]
                    boxy2, boxx2 = hint[1][0], hint[1][1]
                    mainBoard[boxy1][boxx1] = 0
                    mainBoard[boxy2][boxx2] = 0
                    TIMEBONUS += 1
                    alterBoardWithLevel(mainBoard, boxy1, boxx1, boxy2, boxx2, game_lv)

                    if isGameComplete(mainBoard):
                        if draw_completed_game_option() == True:
                            game_lv += 1
                            drawBoard(mainBoard)
                            pygame.display.update()
                            return
                        else:
                            save_game_state(difficulty, game_lv + 1, lives, file_in)
                            return main(player_type, user_acc)


                    if not(mainBoard[boxy1][boxx1] != 0 and bfs(mainBoard, boxy1, boxx1, boxy2, boxx2)):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(100)
                            resetBoard(mainBoard)
                            lives += -1
                            if lives <= 0:
                                pygame.time.wait(1000)
                                game_lv = LEVELMAX + 1
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
                    # if random.randint(0, 100) < 20:
                        # soundObject = random.choice(LIST_SOUNDEFFECT)
                        # soundObject.play()
                    getPointSound.play()
                    mainBoard[firstSelection[1]][firstSelection[0]] = 0
                    mainBoard[boxy][boxx] = 0
                    drawPath(mainBoard, path)
                    TIMEBONUS += 1
                    lastTimeGetPoint = time.time()
                    alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, game_lv)

                    if isGameComplete(mainBoard):
                        if draw_completed_game_option() == True:
                            game_lv += 1
                            drawBoard(mainBoard)
                            pygame.display.update()
                            return
                        else:
                            save_game_state(difficulty, game_lv + 1, lives, file_in)
                            return main(player_type, user_acc)
                        
                            
                    if not(mainBoard[hint[0][0]][hint[0][1]] != 0 and bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(500)
                            resetBoard(mainBoard)
                            lives += -1
                            if lives <= 0:
                                pygame.time.wait(1000)
                                game_lv = LEVELMAX + 1
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
    list_pokemons = list(range(1, len(POKEMONS_DICT) + 1))
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

def main(play_type, user):
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, game_lv, lvl, player_type, user_acc, file_in
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu Classic')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)
    
    # print(play_type, user) 
    
    player_type = play_type
    user_acc = user
    
    if player_type == "guest":
        file_in = "game_state.json"
    elif player_type == "login":
        file_in = "user_info.json"
        
    while True:
        random.shuffle(listBG)
        # random.shuffle(listMusicBG)
        showMenu_Screen()
        game_lv = lvl
        while game_lv <= LEVELMAX:
            runGame()
            pygame.time.wait(1000)
        if game_lv > LEVELMAX and lives > 0:
            showGameModeCompletedScreen()
        else:
            
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
                DISPLAYSURF.blit(POKEMONS_DICT[board[boxy][boxx]], boxRect)

def drawLevel():
    
    level_font = pygame.font.SysFont('Arial', 25,bold=True)
    level_text = level_font.render(f"LEVEL {game_lv}/5", True, ORANGE)
    
    DISPLAYSURF.blit(level_text, ((WINDOWWIDTH // 2) - 50 , barPos[1] + 40))
    
def drawHighlightBox(board, boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 2, top - 2,
                                                   BOXSIZE + 4, BOXSIZE + 4), 2)

def drawClickedBox(board, clickedBoxes):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = POKEMONS_DICT[board[boxy][boxx]].copy()

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
    gameoverFont = pygame.font.Font('freesansbold.ttf', 75)
    gameoverSurf = gameoverFont.render('GAME OVER', True, RED)
    gameoverRect = gameoverSurf.get_rect()
    gameoverRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(gameoverSurf, gameoverRect)
    
    playAgainFont = pygame.font.Font('freesansbold.ttf', 40)
    playAgainSurf = playAgainFont.render('Play Again', True, PURPLE)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (WINDOWWIDTH // 2, (WINDOWHEIGHT // 2) + 100)
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
        pygame.draw.rect(DISPLAYSURF, RED, (left, top,
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
    picRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
    DISPLAYSURF.blit(pic, picRect)
    livesSurf = LIVESFONT.render(str(lives), True, RED)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)

def save_game_state(difficulty, level, lives, filename):
    if player_type == "guest":
        try:
            with open(filename, "r") as file:
                game_state = json.load(file)
        except FileNotFoundError:
            game_state = {}

        game_state[difficulty] = {
            "level": level,
            "lives": lives
        }

        with open(filename, "w") as file:
            json.dump(game_state, file, indent=4)
        
    elif player_type == "login":
            try:
                with open(filename, "r") as file:
                    user_info = json.load(file)
            except FileNotFoundError:
                user_info = {}

            if user_acc not in user_info:
                print(f"Tài khoản '{user_acc}' không tồn tại. Không thể lưu game.")
                return

            if "game_info" not in user_info[user_acc]:
                user_info[user_acc]["game_info"] = {}

            user_info[user_acc]["game_info"][difficulty] = {
                "level": level,
                "lives": lives
            }

            with open(filename, "w") as file:
                json.dump(user_info, file, indent=4)


def load_game_state(difficulty):
    global player_type, user_acc
    if player_type == "guest":
        filename = "game_state.json"
        try:
            with open(filename, "r") as file:
                game_state = json.load(file)

            if difficulty in game_state:
                return game_state[difficulty]
            else:
                return {
                    "level": 1,
                    "lives": 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
                }

        except FileNotFoundError:
            return {
                "level": 1,
                "lives": 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
            }
            
    elif player_type == "login":
        filename = "user_info.json"
        try:
            with open(filename, "r") as file:
                game_data = json.load(file)

            if user_acc in game_data:
                game_info = game_data[user_acc].get("game_info", {})

                if difficulty in game_info:
                    return game_info[difficulty]
                else:
                    return {
                        "level": 1,
                        "lives": 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
                    }
            else:
                return {
                    "level": 1,
                    "lives": 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
                }

        except FileNotFoundError:
            return {
                "level": 1,
                "lives": 3 if difficulty == "easy" else 5 if difficulty == "medium" else 7
            }

def draw_image_button(image, x, y, scale=1):
    
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    scaled_image = pygame.transform.scale(image, (width, height))
    rect = scaled_image.get_rect(topleft=(x, y))
    DISPLAYSURF.blit(scaled_image, rect)
    pygame.display.update()
        
    return rect

def draw_completed_game_option():
    next_lvl_btn = pygame.image.load('./button_image/next_level.png').convert_alpha()
    next_lvl_btnRect = draw_image_button(next_lvl_btn, 505, 270, 0.15)
    back_to_menu_btn = pygame.image.load('./button_image/menu.png').convert_alpha()
    back_to_menu_btnRect = draw_image_button(back_to_menu_btn, 425, 270, 0.15)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if next_lvl_btnRect.collidepoint((mousex, mousey)):
                    next_lvl_btn.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
                    next_lvl_btnRect = draw_image_button(next_lvl_btn, 505, 270, 0.15)
                    pygame.display.update()
                    pygame.time.wait(100)
                    return True
                elif back_to_menu_btnRect.collidepoint((mousex, mousey)):
                    back_to_menu_btn.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
                    back_to_menu_btnRect = draw_image_button(back_to_menu_btn, 425, 270, 0.15)
                    pygame.display.update()
                    pygame.time.wait(100)
                    return False

def showGameModeCompletedScreen(): 
    CongratulationFont = pygame.font.Font('freesansbold.ttf', 50)
    CongratulationSurf = CongratulationFont.render('Congratulation!', True, GREEN)
    CongratulationRect = CongratulationSurf.get_rect()
    CongratulationRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(CongratulationSurf, CongratulationRect)
    pygame.display.update()
    pygame.time.wait(2000)
    return main(player_type, user_acc)
    
def reset_guest_game_state(filename="game_state.json"): 
    if player_type == "guest":
        try:
            with open(filename, "r") as file:
                game_state = json.load(file)
        except FileNotFoundError:
            game_state = {}

        game_state = {
                "easy": {
                        "level": 1,
                        "lives": 3
                    },
                "medium": {
                        "level": 1,
                        "lives": 7
                    },
                "hard": {
                        "level": 1,
                        "lives": 10
                    }
        }

        with open(filename, "w") as file:
            json.dump(game_state, file, indent=4)

    else: 
        pass
    
if __name__ == '__main__':
    initialize_user_info_file()
    start_screen()
