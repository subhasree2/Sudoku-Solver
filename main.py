import pygame
from random import sample
import pygame_widgets
from pygame_widgets.button import Button
import sys

clock = pygame.time.Clock()


def CreateBoard(Board, empties):
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    squares = side * side
    for l in sample(range(squares), empties):
        board[l // side][l % side] = 0
    return board


def DrawGrid():
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # filling the non-empty cells
                pygame.draw.rect(screen, (250, 235, 239, 1.00), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting the default values ; Inserting text
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 15, j * inc + 10))
    # Draw lines horizontally and vertically to form grid
    for i in range(10):
        if i % 3 == 0:
            width = 10  # every 3 small boxes -> thicker line
        else:
            width = 5
        # 500 -> Size of the screen
        pygame.draw.line(screen, (51, 61, 121, 1.00), (i * inc, 0), (i * inc, 500), width)  # vertical
        pygame.draw.line(screen, (51, 61, 121, 1.00), (0, i * inc), (500, i * inc), width)  # horizontal


# Solving using Backtracking Algorithm
def SolveGrid(gridArray, i, j):
    global IsSolving
    IsSolving = True
    while gridArray[i][j] != 0:  # cell is not empty
        # this while loop allows us to go through the entire grid
        if i < 8:  # still in the first row, just go through all the columns
            i += 1
        elif i == 8 and j < 8:  # go back to the first column and next row
            i = 0
            j += 1
        elif i == 8 and j == 8:  # went through entire thing
            return True
    pygame.event.pump()  # called once every loop
    for V in range(1, 10):  # trying values from 1->9 inclusive
        if IsUserValueValid(gridArray, i, j, V):  # if the value is correct, add it to the grid
            gridArray[i][j] = V
            if SolveGrid(gridArray, i, j):  # if the value is correct, keep it
                return True
            else:  # else keep the box empty
                gridArray[i][j] = 0
        screen.fill((255, 255, 255))
        DrawGrid()
        DrawSelectedBox()
        DrawModes()
        DrawSolveButton()
        pygame.display.update()
    return False


# setting the initial position
def SetMousePosition(p):
    global x, y
    if p[0] < 500 and p[1] < 500:
        x = p[0] // inc
        y = p[1] // inc


# checks if inserted val is valid
def IsUserValueValid(m, i, j, v):
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v:  # checks cols and rows
            return False
    # checks the box/block
    ii = i // 3
    jj = j // 3
    for i in range(ii * 3, ii * 3 + 3):
        for j in range(jj * 3, jj * 3 + 3):
            if m[i][j] == v:
                return False
    return True


# highlighting the selected cell
def DrawSelectedBox():
    for i in range(2):
        pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)  # Horizontal
        pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)  # Vertical


# insert value entered by user
def InsertValue(Value):
    grid[int(x)][int(y)] = Value
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))


def IsUserWin():
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True


def DrawModes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Procedure :-", True, (0, 0, 0)), (540, 10))
    screen.blit(AttributeFont.render("Let's start our morning with Sudoku : ", True, (0, 0, 0)), (540, 40))
    screen.blit(AttributeFont.render("1. Press 'E' for Easy , 'A' for Average and 'H' for Hard Mode", True, (0, 0, 0)),
                (550, 80))
    screen.blit(AttributeFont.render("2. Get Ready and start solving!", True, (0, 0, 0)), (550, 120))
    screen.blit(
        AttributeFont.render("3. Couldn't Solve ? Click 'Solve' to solve Sudoku Automatically", True, (0, 0, 0)),
        (550, 160))

    screen.blit(TitleFont.render("Modes :-", True, (0, 0, 0)), (545, 200))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (550, 240))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (550, 270))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (550, 300))

    screen.blit(AttributeFont.render("One more game ? Choose the mode and start!!", True, (0, 0, 0)), (610, 465))


def DrawSolveButton():
    events = pygame.event.get()
    button = Button(
        screen, 670, 380, 270, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(250, 235, 239, 1.00),
        pressedColour=(51, 61, 121, 1.00), radius=20,
        onClick=lambda: SolveGrid(grid, 0, 0))
    pygame_widgets.update(events)
    pygame.display.update()


def DisplayMessage(Message, Interval, Color):
    screen.blit(a_font.render(Message, True, Color), (690, 330))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()


def SetGridMode(Mode):
    global grid
    screen.fill((255, 255, 255))
    events = pygame.event.get()
    DrawModes()
    DrawSolveButton()
    if Mode == 0:  # For clearing the grid
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        pygame_widgets.update(events)
        pygame.display.update()
    elif Mode == 1:  # For easy mode
        grid = CreateBoard([], 23)
    elif Mode == 2:  # For average mode
        grid = CreateBoard([], 27)
    elif Mode == 3:  # For hard mode
        grid = CreateBoard([], 30)
    Button_Press_Time = pygame.time.get_ticks()


def HandleEvents():
    global IsRunning, grid, x, y, UserValue
    events = pygame.event.get()
    for event in events:
        # Quit the game window
        if event.type == pygame.QUIT:
            IsRunning = False
            sys.exit()
        # Get the mouse position to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            SetMousePosition(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if IsRunning:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1
                if event.key == pygame.K_1:
                    UserValue = 1
                if event.key == pygame.K_2:
                    UserValue = 2
                if event.key == pygame.K_3:
                    UserValue = 3
                if event.key == pygame.K_4:
                    UserValue = 4
                if event.key == pygame.K_5:
                    UserValue = 5
                if event.key == pygame.K_6:
                    UserValue = 6
                if event.key == pygame.K_7:
                    UserValue = 7
                if event.key == pygame.K_8:
                    UserValue = 8
                if event.key == pygame.K_9:
                    UserValue = 9
                if event.key == pygame.K_c:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
    button = Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: SolveGrid(grid, 0, 0))
    pygame_widgets.update(events)
    pygame.display.update()


def DrawUserValue():
    global UserValue, IsSolving
    if UserValue > 0:
        if IsUserValueValid(grid, x, y, UserValue):
            if grid[int(x)][int(y)] == 0:
                InsertValue(UserValue)
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("YOU WON!!!!", 5000, (0, 255, 0))

            else:
                UserValue = 0
        else:
            DisplayMessage("Incorrect Value", 500, (255, 0, 0))
            UserValue = 0


def InitializeComponent():
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawSolveButton()
    pygame.display.update()


def GameThread():
    InitializeComponent()
    while IsRunning:
        HandleEvents()
        DrawGrid()
        DrawSelectedBox()
        DrawUserValue()
        pygame.display.update()


if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((1100, 505))  # Window size
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Let's play Sudoku🙂")
    a_font = pygame.font.SysFont("times", 30, "bold")  # Different fonts to be used
    b_font = pygame.font.SysFont("times", 25, "bold")
    inc = 500 // 9  # Screen size // Number of boxes = each increment
    x = 0
    currentTime = 0
    y = 0
    UserValue = 0
    grid = CreateBoard([], 17)
    IsRunning = True
    IsSolving = False
    GameThread()
