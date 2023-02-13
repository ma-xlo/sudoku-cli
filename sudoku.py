#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import system
from random import randint
import boards_databases
from termcolor import colored, cprint
import copy
import re
import sys


#==================== Levels ====================#
EASY_LEVEL = 3
MEDIUM_LEVEL = 6
HARD_LEVEL = 9
EXTREME_LEVEL = 15
#================= Table frames =================#
VERTICAL_BAR_GREEN = colored('│', 'green')
VERTICAL_DOTED_BAR_GREEN = colored('¦', 'green')

def convertToInt(number):
    if(number == '\u278A'):
        return 1
    elif(number == '\u278B'):
        return 2
    elif(number == '\u278C'):
        return 3
    elif(number == '\u278D'):
        return 4
    elif(number == '\u278E'):
        return 5
    elif(number == '\u278F'):
        return 6
    elif(number == '\u2790'):
        return 7
    elif(number == '\u2791'):
        return 8
    elif(number == '\u2792'):
        return 9

def check_table(game_board, solved_board):
    for i in range(9):
        for j in range(9):
            if game_board[i][j] != solved_board[i][j] and  not game_board[i][j] == ' ':
                return 'invalid'
    return 'valid'

def game_messages (type):
    if type == 'valid':
        return colored('                  \u2714 All good!', 'green')
    elif type == 'invalid': 
        return colored('               Board not valid!', 'red')
    elif type == 'error': 
        return colored('              Invalid insertion!', 'red')
    elif type == 'unknown': 
        return colored('              Command not found', 'red')
    
def level_generator(option):
    if option == 1:
        return randint(EASY_LEVEL, EASY_LEVEL)
    elif option == 2:
        return randint(MEDIUM_LEVEL, MEDIUM_LEVEL)
    elif option == 3:
        return randint(HARD_LEVEL, HARD_LEVEL)
    elif option == 4:
        return randint(EXTREME_LEVEL, EXTREME_LEVEL)


x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
y_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9]
insert_numbers = ['\u278A', '\u278B', '\u278C', '\u278D', '\u278E', '\u278F', '\u2790', '\u2791', '\u2792']
subscript_numbers = ['\u00B9', '\u00B2', '\u00B3','\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079']


while True:
    # solved_board = boards_databases.boards[0]
    solved_board = boards_databases.boards[randint(0, len(boards_databases.boards) - 1)]
    board = copy.deepcopy(solved_board)
    message = False
    message_type = ''

    while(True):
        system('clear')
        print('\n\n')
        print('              🆂 🆄 🅳 🄾 🅺 🆄')
        print('                 🅲 🅻 🅸\n')
        print('              [1] New game           ')
        print('              [2] Help               ')
        print('              [3] Exit               ')
        print('')
        option = str(input('               Option: '))

        if option[0] >= '1' or option[0] <= '3' and len(option) == 1:
            break
    
    if(option == '1'):
        while(True):
            system('clear')
            print('\n\n')
            print('             Choose difficult:     \n')
            print('               [1] Easy               ')
            print('               [2] Medium             ')
            print('               [3] Hard               ')
            print('               [4] Extreme               ')
            print('')
            level_option = str(input('               Option: '))
            
            if level_option[0] >= '1' or level_option[0] <= '3' and len(level_option) == 1:
                break

        for i in range(9):
            level = level_generator(int(level_option))
            for j in range(level):
                random_index = randint(0, 9)
                board[i][random_index - 1] = ' '
        game_board = copy.deepcopy(board)
        reset_game_board = copy.deepcopy(board)
        
        while True:
            system('clear')
            print()
            print('  ┌───────────────────────────────────────┐')
            print('  │               SUDOKU-CLI              │')
            print('  ├───┬───┬───┬───┬───┬───┬───┬───┬───┬───┤')
            print('  │ # │ A │ B │ C │ D │ E │ F │ G │ H │ I │')
            print('  ├───┼───┴───┴───┴───┴───┴───┴───┴───┴───┤')

            for i in range(9):
                print(end=' ')
                
                print(f' │ {y_axis[i]} │', end= ' ')
                for j in range(9):
                    if not j == 8 and not j == 2 and not j == 5:
                        print(f'{board[i][j]} {VERTICAL_DOTED_BAR_GREEN}', end= ' ')
                    elif j == 2 or j == 5:
                        print(f'{board[i][j]} │', end= ' ')
                    else:
                        print(f'{board[i][j]}', end= ' ')
                if j == 8:
                    print('│')
                if i == 2 or i == 5:
                    print('  │ - │ ──────────┼───────────┼────────── │')
            print('  └───┴───────────────────────────────────┘')
            
            if message:
                print(game_messages(message_type))
                message = False
            else:
                print()

            cmd_input = str(input('                  Command: '))

            if cmd_input == 'check':
                message = True
                message_type = check_table(game_board, solved_board);

            elif cmd_input == 'clear':
                game_board = copy.deepcopy(reset_game_board)
                board = copy.deepcopy(reset_game_board)

            elif cmd_input == 'quit':
                break

            elif re.search(r'[a-i][1-9]-[1-9]', cmd_input):
                x = cmd_input[0]
                y = int(cmd_input[1])
                n = int(cmd_input[3])
                for i in range(len(x_axis)):
                    if(x == x_axis[i]):
                        if(n < 1 or n > 9):
                            continue
                        elif(board[y-1][i] == ' ' or isinstance(board[y-1][i], str)):
                            board[y-1][i] = insert_numbers[n-1]
                            game_board[y-1][i] = convertToInt(insert_numbers[n-1])

            else:
                message = True
                message_type = 'unknown'

            if game_board == solved_board:
                system('clear')
                print()
                print(colored('  ┌───────────────────────────────────────┐', 'green'))
                print(colored('  │               SUDOKU-CLI              │', 'green'))
                print(colored('  ├───┬───┬───┬───┬───┬───┬───┬───┬───┬───┤', 'green'))
                print(colored('  │ # │ A │ B │ C │ D │ E │ F │ G │ H │ I │', 'green'))
                print(colored('  ├───┼───┴───┴───┴───┴───┴───┴───┴───┴───┤', 'green'))

                for i in range(9):
                    print(end=' ')
                    number = colored(str(y_axis[i]), 'green')
                    print(f' {VERTICAL_BAR_GREEN} {number} {VERTICAL_BAR_GREEN}', end= ' ')
                    for j in range(9):
                        if not j == 8 and not j == 2 and not j == 5:
                            number = colored(str(solved_board[i][j]), 'green')
                            print(f'{number} {VERTICAL_DOTED_BAR_GREEN}', end= ' ')
                        elif j == 2 or j == 5:
                            number = colored(str(solved_board[i][j]), 'green')
                            print(f'{number} {VERTICAL_BAR_GREEN}', end= ' ')
                        else:
                            number = colored(str(solved_board[i][j]), 'green')
                            print(f'{number}', end= ' ')
                    if j == 8:
                        print(VERTICAL_BAR_GREEN)
                    if i == 2 or i == 5:
                        print(colored('  │ - │ ──────────┼───────────┼────────── │', 'green'))
                print(colored('  └───┴───────────────────────────────────┘\n', 'green'))
                print('             🏆 Congratulations!              \n')
                input('       Press enter to return to menu...')
                break

    if(option == '2'):
        system('clear')
        print('\n\n')
        print(' In game commands:')
        print(' [X AXIS][Y AXIS]-[NUMBER]       insert a number')
        print(' check                           validate the table ')
        print(' clear                           clear the table')
        print(' quit                            leave the game\n')
        input(' Press Enter to return...')
    if(option == '3'):
        break

    

