import pygame
import boards_databases
from random import randint
import copy
import re

# Configurações do Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Tamanho da tela
WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Tamanho da grade
CELL_SIZE = WIDTH // 9

# Fontes
FONT = pygame.font.Font(None, 40)
BIG_FONT = pygame.font.Font(None, 80)

# Níveis de dificuldade
EASY_LEVEL = 3
MEDIUM_LEVEL = 6
HARD_LEVEL = 9
EXTREME_LEVEL = 15

def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            line_width = 4
        else:
            line_width = 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)

def draw_numbers(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != ' ':
                text = FONT.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 10))

def draw_selected(x, y):
    if x is not None and y is not None:
        pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def draw_message(message):
    text = BIG_FONT.render(message, True, GREEN)
    screen.blit(text, (WIDTH // 6, HEIGHT // 2))

def convertToInt(number):
    return int(number)

def check_table(game_board, solved_board):
    for i in range(9):
        for j in range(9):
            if game_board[i][j] != solved_board[i][j] and not game_board[i][j] == ' ':
                return 'invalid'
    return 'valid'

def level_generator(option):
    if option == 1:
        return randint(EASY_LEVEL, EASY_LEVEL)
    elif option == 2:
        return randint(MEDIUM_LEVEL, MEDIUM_LEVEL)
    elif option == 3:
        return randint(HARD_LEVEL, HARD_LEVEL)
    elif option == 4:
        return randint(EXTREME_LEVEL, EXTREME_LEVEL)

def main():
    running = True
    selected_x, selected_y = None, None
    solved_board = boards_databases.boards[randint(0, len(boards_databases.boards) - 1)]
    board = copy.deepcopy(solved_board)
    game_board = copy.deepcopy(board)
    reset_game_board = copy.deepcopy(board)
    message = ""
    level_option = 1  # Default para fácil

    for i in range(9):
        level = level_generator(level_option)
        for j in range(level):
            random_index = randint(0, 9)
            board[i][random_index - 1] = ' '

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers(board)
        draw_selected(selected_x, selected_y)
        if message:
            draw_message(message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_x, selected_y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    board[selected_y][selected_x] = 1
                    game_board[selected_y][selected_x] = 1
                elif event.key == pygame.K_2:
                    board[selected_y][selected_x] = 2
                    game_board[selected_y][selected_x] = 2
                elif event.key == pygame.K_3:
                    board[selected_y][selected_x] = 3
                    game_board[selected_y][selected_x] = 3
                elif event.key == pygame.K_4:
                    board[selected_y][selected_x] = 4
                    game_board[selected_y][selected_x] = 4
                elif event.key == pygame.K_5:
                    board[selected_y][selected_x] = 5
                    game_board[selected_y][selected_x] = 5
                elif event.key == pygame.K_6:
                    board[selected_y][selected_x] = 6
                    game_board[selected_y][selected_x] = 6
                elif event.key == pygame.K_7:
                    board[selected_y][selected_x] = 7
                    game_board[selected_y][selected_x] = 7
                elif event.key == pygame.K_8:
                    board[selected_y][selected_x] = 8
                    game_board[selected_y][selected_x] = 8
                elif event.key == pygame.K_9:
                    board[selected_y][selected_x] = 9
                    game_board[selected_y][selected_x] = 9
                elif event.key == pygame.K_RETURN:
                    message = check_table(game_board, solved_board)
                elif event.key == pygame.K_BACKSPACE:
                    game_board = copy.deepcopy(reset_game_board)
                    board = copy.deepcopy(reset_game_board)
                elif event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()
