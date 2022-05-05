
import numpy as np
import random
import pygame
import sys

ROW_COUNT = 6
COL_COUNT = 7

WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
colors = [WHITE, RED, YELLOW]

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
EMPTY = 0


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

        # check win for each row
        for i in range(ROW_COUNT):
            row = board[i]
            # for each window of 4
            for j in range(4):
                window = row[j:j+4]
                if not np.any(window - piece):
                    return "Player " + str(piece) + " wins!!"

        # check win for each column
        for i in range(COL_COUNT):
            col = board[:,i]
            # for each window of 4
            for j in range(3):
                window = col[j:j+4]
                if not np.any(window - piece):
                    return "Player " + str(piece) + " wins!!"

        # check win for the diagonals
        # offsets from -2 to 2
        for i in range(-2,4):
            diag = np.diagonal(board,i)
            for j in range(len(diag)-3):
                window = diag[j:j+4]
                if not np.any(window - piece):
                    return "Player " + str(piece) + " wins!!"

        # check win for the diagonals in the other direction
        # offsets from -2 to 2
        temp = np.flip(board.copy(), axis=1)
        for i in range(-2, 4):
            diag = np.diagonal(temp, i)
            for j in range(len(diag) - 3):
                window = diag[j:j + 4]
                if not np.any(window - piece):
                    return "Player " + str(piece) + " wins!!"
    return False


def eval_window(window, piece):
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    score = 0
    if window.count(piece) == 4:
        score += 1000
    if window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    if window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 4:
        score -= 100
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80


    return score


def score_position(board, piece):
    score = 0

    # score center
    center_arr = [int(i) for i in list(board[:,COL_COUNT//2])]
    score += center_arr.count(piece) * 3

    # score horizontal
    for r in range(ROW_COUNT):
        row_arr = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            window = row_arr[r:r+WINDOW_LENGTH]
            score += eval_window(window, piece)
    # score vertical
    for c in range(COL_COUNT):
        col_arr = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_arr[r:r+WINDOW_LENGTH]
            score += eval_window(window, piece)

    # score diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += eval_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += eval_window(window, piece)

    return score


def is_terminal_node(board):
    return (False if not check_win(board) else True) or len(get_valid_locs(board)) == 0


def minimax(board, depth, maximizing_player):
    valid_locs = get_valid_locs(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board) == "Player 2 wins!!":
                return None, 100000
            elif check_win(board) == "Player 1 wins!!":
                return None, -100000
            else: # game over
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)
    if maximizing_player:
        score = -100000
        col = random.choice(valid_locs)
        for c in valid_locs:
            r = get_next_open_row(board, c)
            temp_board = board.copy()
            drop_piece(temp_board, r, c, AI_PIECE)
            new_score = minimax(temp_board, depth-1, False)[1]
            if new_score > score:
                score = new_score
                col = c
        return col, score
    else:
        score = 100000
        col = random.choice(valid_locs)
        for c in valid_locs:
            r = get_next_open_row(board, c)
            temp_board = board.copy()
            drop_piece(temp_board, r, c, PLAYER_PIECE)
            new_score = minimax(temp_board, depth-1, True)[1]
            if new_score < score:
                score = new_score
                col = c
        return col, score


def get_valid_locs(board):
    valid_loc = []
    for c in range(COL_COUNT):
        if is_valid_column(board, c):
            valid_loc.append(c)

    return valid_loc


def pick_best_move(board, piece):
    valid_locs = get_valid_locs(board)
    best_score = -100000
    best_col = random.choice(valid_locs)
    for c in valid_locs:
        r = get_next_open_row(board, c)
        temp_board = board.copy()
        drop_piece(temp_board, r, c, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = c

    return best_col


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(1,ROW_COUNT+1):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, colors[int(board[r-1][c])], (c*SQUARESIZE + SQUARESIZE//2, r*SQUARESIZE + SQUARESIZE//2), RADIUS)


board = create_board()
game_over = False
turn = random.randint(PLAYER, AI)

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
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            pygame.draw.circle(screen, RED, (event.pos[0], SQUARESIZE//2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ask for player 1 input
            if turn == PLAYER:
                col = event.pos[0] // SQUARESIZE
                while not is_valid_column(board, col):
                    col = int(input("Player 1, make your selection (0-6): "))
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                turn += 1
                turn = turn % 2
                draw_board(board)
                pygame.display.update()

                win = check_win(board)
                if win:
                    label = myfont.render(win, 1, (255,255,255))
                    screen.blit(label, (30,10))
                    game_over = True

    ## AI turn
    if turn == AI and not game_over:
        # col = random.randint(0, COL_COUNT - 1)
        # col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 3, True)
        while not is_valid_column(board, col):
            col = pick_best_move(board, AI_PIECE)

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)

        print(board)

        win = check_win(board)
        if win:
            label = myfont.render(win, 1, (255,255,255))
            screen.blit(label, (30,10))
            game_over = True

        turn += 1
        turn = turn % 2

        # pygame.time.wait(300)
        draw_board(board)
        pygame.display.update()

        if game_over:
            pygame.time.wait(3000)
