#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import system
from random import randint
import boards_databases
from termcolor import colored
import copy
import re
import sys
import ctypes
import ctypes.wintypes as wintypes
import keyboard
import time
import threading
from playsound import playsound


import os
os.system('mode con lines=22 cols=45')

# Constants
GWL_STYLE = -16
WS_MAXIMIZEBOX = 0x00010000

# Define Windows API functions
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Get window handle by title
user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
user32.FindWindowW.restype = wintypes.HWND

# Get and set window long
user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
user32.GetWindowLongW.restype = ctypes.c_long

user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
user32.SetWindowLongW.restype = ctypes.c_long

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

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

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

def show_help():
    system('cls')
    print('\n\n')
    print(' ┌─────────────────────────────────────────┐')
    print(' │                   HELP                  │')
    print(' ├─────────────────────────────────────────┤')
    print(' │ Insert a number ......... a1-5|c6-2|b3-5│')
    print(' │ Validate board .......... check         │')
    print(' │ Clear board ............. clear         │')
    print(' │ Leave the game .......... exit          │')
    print(' └─────────────────────────────────────────┘')
    print()
    print()
    input('          Press Enter to return...')

def play_sound():
    playsound('./intro.mp3')

def splash_screen():
    hide_cursor()
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    print('\n\n\n\n')
    print(colored('   ██████╗   █████╗██╗     ██╗ ██╗███╗   ██╗ ', 'red'))
    print(colored('  ██╔════╝ ██╔══██╗██║     ██║███║████╗  ██║', 'yellow'))
    print(colored('  ██║  ███╗███████║██║     ██║╚██║██╔██╗ ██║', 'green'))
    print(colored('  ██║   ██║██╔══██║██║██   ██║ ██║██║╚██╗██║', 'cyan'))
    print(colored('  ╚██████╔╝██║  ██║██║╚█████╔╝ ██║██║ ╚████║', 'blue'))
    print(colored('  ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚════╝  ╚═╝╚═╝  ╚═══╝ ', 'magenta'))
    print('                GAME STUDIOS                ')
    print('\n')
    
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.start()

    for i in range(10):
        time.sleep(0.35)
        sys.stdout.write(colored("\r                " + animation[i % len(animation)], 'white'))
        sys.stdout.flush()
    
    sound_thread.join()
def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\n\n\n')
        print(colored('                  ┌─┬─┬─┬─┐     ', 'cyan')) 
        print(colored('                  │M│I│N│I│     ', 'cyan'))   
        print(colored('                ┌─┼─┼─┼─┼─┼─┐   ', 'blue')) 
        print(colored('                │S│U│D│O│K│U│   ', 'blue')) 
        print(colored('              ┌───────────────┐ ', 'white')) 
        print(colored('              │  [1] New game │ ', 'white')) 
        print(colored('              │  [2] Help     │ ', 'white')) 
        print(colored('              │  [3] Exit     │ ', 'white')) 
        print(colored('              └───────────────┘ ', 'white')) 
        print('')
        
        option = None
        while option not in ['1', '2', '3']:
            option = str(input("                  Option: "))
        return option


def difficulty_menu():
    while(True):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\n\n\n')
        print(colored('                  ┌─┬─┬─┬─┐     ', 'cyan')) 
        print(colored('                  │M│I│N│I│     ', 'cyan'))  
        print(colored('                ┌─┼─┼─┼─┼─┼─┐   ', 'blue')) 
        print(colored('                │S│U│D│O│K│U│   ', 'blue')) 
        print(colored('              ┌───────────────┐ ', 'white')) 
        print(colored('              │  [1] Easy     │ ', 'white')) 
        print(colored('              │  [2] Medium   │ ', 'white')) 
        print(colored('              │  [3] Hard     │ ', 'white')) 
        print(colored('              │  [4] Extreme  │ ', 'white')) 
        print(colored('              └───────────────┘ ', 'white')) 
        print('')
        
        level_option = None
        option = None
        while option not in ['1', '2', '3', '4']:
            option = str(input("                  Option: "))
        return option
        return level_option

#
# Game initialization
#
splash_screen()
show_cursor()

while True:
    x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    y_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    insert_numbers = [
        colored(1, 'yellow'),
        colored(2, 'yellow'),
        colored(3, 'yellow'),
        colored(4, 'yellow'),
        colored(5, 'yellow'),
        colored(6, 'yellow'),
        colored(7, 'yellow'), 
        colored(8, 'yellow'),
        colored(9, 'yellow'),
    ]
    # insert_numbers = ['\u278A', '\u278B', '\u278C', '\u278D', '\u278E', '\u278F', '\u2790', '\u2791', '\u2792']
    subscript_numbers = ['\u00B9', '\u00B2', '\u00B3','\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079']
    solved_board = boards_databases.boards[0]
    solved_board = boards_databases.boards[randint(0, len(boards_databases.boards) - 1)]
    board = copy.deepcopy(solved_board)
    message = False
    message_type = ''
    option = main_menu()

    level_option=0
    if(option == '1'):
        level_option = difficulty_menu()
    if(option == '2'):
        show_help()
        continue
    elif(option == '3'):
        exit(0)

    for i in range(9):
        level = level_generator(int(level_option))
        for j in range(level):
            random_index = randint(0, 9)
            board[i][random_index - 1] = ' '
    game_board = copy.deepcopy(board)
    reset_game_board = copy.deepcopy(board)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        print('  ┌───────────────────────────────────────┐')
        print('  │                 SUDOKU                │')
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
        cmd_input = str(input('               Coordinates: '))

        if cmd_input == 'validate':
            message = True
            message_type = check_table(game_board, solved_board)

        elif cmd_input == 'clear':
            game_board = copy.deepcopy(reset_game_board)
            board = copy.deepcopy(reset_game_board)

        elif cmd_input == 'exit':
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
            print()
            print(colored('  ┌───────────────────────────────────────┐', 'green'))
            print(colored('  │                 SUDOKU                │', 'green'))
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





