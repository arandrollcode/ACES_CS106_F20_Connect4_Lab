import pygame
import sys
import math
import tkinter

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = list()

    for _ in range(COLUMN_COUNT):
        board.append([0] * ROW_COUNT)
    
    return board

def drop_piece(board, col, row, piece):
    board[col][row] = piece

def is_valid_column(board, col):
    return board[col][0] == 0

def get_next_open_row(board, col):
    for row in range(ROW_COUNT, 0, -1):
        if board[col][row-1] == 0:
            return row-1

def print_board(board):
    print('-----------------')
    
    for row in range(ROW_COUNT):
        print('| {0} {1} {2} {3} {4} {5} {6} |'.format(board[0][row], board[1][row], board[2][row], board[3][row], board[4][row], board[5][row], board[6][row]))

    print('-----------------')
    print()
    
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[c][r] == piece and board[c+1][r] == piece and board[c+2][r] == piece and board[c+3][r] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[c][r] == piece and board[c][r+1] == piece and board[c][r+2] == piece and board[c][r+3] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[c][r+3] == piece and board[c+1][r+2] == piece and board[c+2][r+1] == piece and board[c+3][r] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[c][r] == piece and board[c+1][r+1] == piece and board[c+2][r+2] == piece and board[c+3][r+3] == piece:
                return True

    return False

def draw_board(board):
    ## TODO: Draw a large WHITE rectangle (7 SQUARESIZE Wide, 6 SQUARESIZE Tall)
    
    
    b_copy = [list(board[col]) for col in range(COLUMN_COUNT)]
    for col in b_copy:
        col.reverse()

    ## TODO: Draw the 42 circles based on b_copy


    ## TODO: Update the display

##----------------------------------------------------------------------------##

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        ## Tracks piece to follow mouse
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_column(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, col, row, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
            ## Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_column(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, col, row, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 2, BLACK)
                        screen.blit(label, (40,10))
                        game_over = True
                        
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            flag = False

            for col in range(COLUMN_COUNT):
                if is_valid_column(board, col):
                    flag = True

            if flag == False:
                label = myfont.render("Tie Game!!", 2, BLUE)
                screen.blit(label, (40,10))
                game_over = True
                print_board(board)
                draw_board(board)

            if game_over:
                ## OPTIONAL TODO: Display a tkinter message box asking the user if they want to reset for a new game.
                pygame.time.wait(3000)

                
