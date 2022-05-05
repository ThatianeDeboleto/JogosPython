
import numpy as np
import pygame
import sys

ROW_COUNT = 6
COL_COUNT = 7

WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
colors = [WHITE, RED, BLUE]


def create_board():
    return np.zeros((6, 7))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_column(board, col):
    if col >= 0 and col <= 6 and board[0][col] == 0:
        return True
    else:
        return False


def get_next_open_row(board, col):
    for i in range(ROW_COUNT-1, -1, -1):
        if board[i][col] == 0:
            return i


def check_win(board):
    for piece in [1,2]:


        for i in range(ROW_COUNT):
            row = board[i]

            for j in range(4):
                window = row[j:j+4]
                if not np.any(window - piece):
                    return "Jogador " + str(piece) + " vitórias!!"


        for i in range(COL_COUNT):
            col = board[:,i]

            for j in range(3):
                window = col[j:j+4]
                if not np.any(window - piece):
                    return "Jogagor " + str(piece) + " vitórias!!"


        for i in range(-2,2):
            diag = np.diagonal(board,i)
            for j in range(len(diag)-3):
                window = diag[j:j+4]
                if not np.any(window - piece):
                    return "Jogador " + str(piece) + " é o vencedor!"


        temp = np.flip(board.copy(), axis=1)
        for i in range(-2, 2):
            diag = np.diagonal(temp, i)
            for j in range(len(diag) - 3):
                window = diag[j:j + 4]
                if not np.any(window - piece):
                    return "Jogador " + str(piece) + " é o vencedor!"
    return False


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(1,ROW_COUNT+1):
            pygame.draw.rect(screen, BLACK, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, colors[int(board[r-1][c])], (c*SQUARESIZE + SQUARESIZE//2, r*SQUARESIZE + SQUARESIZE//2), RADIUS)

board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = SQUARESIZE//2 - 5

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
            pygame.draw.circle(screen, RED if turn == 0 else BLUE, (event.pos[0], SQUARESIZE//2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ask for player 1 input
            if turn == 0:
                col = event.pos[0] // SQUARESIZE
                while not is_valid_column(board, col):
                    col = int(input("Jogador 1, faça sua seleção (0-6): "))
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)


            else:
                col = event.pos[0] // SQUARESIZE
                while not is_valid_column(board, col):
                    col = int(input("Jogador 2, faça sua seleção (0-6): "))
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

            print(board)

            win = check_win(board)
            if win:
                label = myfont.render(win, 1, (255,255,255))
                screen.blit(label, (30,10))
                game_over = True

            turn += 1
            turn = turn % 2

            draw_board(board)
            pygame.display.update()

            if game_over:
                pygame.time.wait(3000)
