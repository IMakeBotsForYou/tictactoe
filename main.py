'''
Code by https://github.com/IMakeBotsForYou/
'''
import tkinter as tk
from tkinter import messagebox
import random

ROWS = 3
COLUMNS = 3
# Creates an empty board

board = {}
corners = ["00", "02", "20", "22"]
middles = ["01", "10", "21", "12"]
already_countered = False


def initialize_board():
    for i in range(ROWS):
        for j in range(COLUMNS):
            board[f'{i}{j}'] = " "


turn = "X"
user = "X"

counter = 0  # make it so bot runs instantly when playing as "O"


def make_move(button, row, column, root):
    global turn, user, counter
    turn = "X"  # runs once
    counter += 1
    if counter == 9 and user == "O":
        print("Bot first")
        move = bot_move(board)
        disable_btn(buttons[move[0] * 3 + move[1]], move[0], move[1], root)

    def move():
        disable_btn(button, row, column, root)
        move = bot_move(board)
        try:
            disable_btn(buttons[move[0] * 3 + move[1]], move[0], move[1], root)
        except:
            print("Game end.")  # bot crashes when game ends so this solves it ;)

    return move


def disable_btn(button, row, column, root):
    global turn, user
    button["state"] = tk.DISABLED
    button["text"] = turn
    button["font"] = ("Courier", 24)
    button["fg"] = "black"
    board[f'{row}{column}'] = turn

    if f'{row}{column}' in corners:
        del corners[corners.index(f'{row}{column}')]

    elif f'{row}{column}' in middles:
        del middles[middles.index(f'{row}{column}')]

    if winner(board, turn):
        messagebox.showinfo("Winner", f'{turn} has won')
        root.destroy()
    elif is_full(board):
        messagebox.showinfo("No Winner", 'Tie')
        root.destroy()
    turn = "X" if turn == "O" else "O"


def is_free(i, j):
    return board[f'{i}{j}'] == " "


def free_spaces(b):
    return len([i for i, j in b.items() if b[f'{i}'] == " "])


def equal4(a, b, c, d):
    return True if a == b and a == c and a == d else False


def corner_fork():  # check if bot is being forked
    corner_played = [key for key, value in board.items() if value == user and key in ["00", "02", "20", "22"]]
    if len(corner_played) > 0:
        corner_played = corner_played[0]
        op = ["00", "02", "20", "22"][3-["00", "02", "20", "22"].index(corner_played)]
        return True if board[op] == user else False
    else:
        return False

def side_fork():  # find out what corner needs to be played in order to prevent fork
    middles_played = [key for key, value in board.items() if value == user and key in ["01", "10", "21", "12"]]
    if len(middles_played) == 2:
        if middles_played[0] == "01" and middles_played[1] == "12":
            return "02"
        elif middles_played[0] == "01" and middles_played[1] == "10":
            return "00"
        elif middles_played[0] == "12" and middles_played[1] == "21":
            return "22"
        elif middles_played[0] == "10" and middles_played[1] == "21":
            return "20"
        else:
            return "No Fork"
    else:
        return "No Fork"

def bot_move(b):  # b = board
    global user, already_countered
    move = 0, 0
    # can we win the next move? can user win next move?
    for i in range(3):
        for j in range(3):
            if is_free(i, j):
                copy = board.copy()

                copy[f'{i}{j}'] = turn
                if winner(copy, turn):
                    return i, j

                copy[f'{i}{j}'] = user
                if winner(copy, user):
                    return i, j
    # user first      #only first round  #middle is free    #user has taken one of corners, so we need to counter
    if user == "X" and free_spaces(b) == 8 and is_free(1, 1):
        return 1, 1
    # are we being forked?

    # try to take corners if free
    if len(corners) > 0 and not corner_fork():
        # counter first corner with
        try:
            fork_ch = side_fork()
            if not fork_ch == "No Fork" and not already_countered:
                move = [fork_ch]
                already_countered = True
            else:
                move = random.sample(corners, 1)
        except:
            print("Error")
        return int(move[0][0]), int(move[0][1])
    elif len(middles) > 0:
        # move to sides
        move = random.sample(middles, 1)
        return int(move[0][0]), int(move[0][1])
    #return random
    a = [x for x in board.keys() if board[x] == " "]
    if len(a) > 0:
        move = random.sample(a, 1)
        return int(move[0][0]), int(move[0][1])
    return -1, -1


# Inspired by Yakov's design.
def make_resizable(rows, columns, a):
    for x in range(columns):
        tk.Grid.columnconfigure(a, x, weight=1)
    for y in range(rows):
        tk.Grid.rowconfigure(a, y, weight=1)


# Check the board is full or not
def is_full(b):
    return sum(value == ' ' for value in b.values()) == 0


def display(b):
    for x in range(3):
        for y in range(3):
            print(b[f'{x}{y}'], end=" ")
        print()


# Check l(O/X) won the match or not
# according to the rules of the game
def winner(b, char):
    for x in range(3):
        # check horizontal lines
        if equal4(b[f"{x}0"], b[f"{x}1"], b[f"{x}2"], char):
            return True
        # check vertical lines
        if equal4(b[f"0{x}"], b[f"1{x}"], b[f"2{x}"], char):
            return True
        # check top left to bottom right diagonal line
    if equal4(b[f"00"], b[f"11"], b[f"22"], char):
        return True
        # check bottom left to top right diagonal line
    if equal4(b[f"20"], b[f"11"], b[f"02"], char):
        return True
    return False


buttons = []


def play(root, t):
    global turn, user, buttons
    turn = t
    user = t
    root.destroy()
    root = tk.Tk()
    root.geometry("750x750")
    for i in range(ROWS):
        for j in range(COLUMNS):
            btn = tk.Button(root, text=' ', relief="groove")
            buttons.append(btn)
            btn.configure(command=make_move(btn, i, j, root))
            btn.grid(row=i, column=j, sticky="eswn")  # sticky=tk.E+tk.W+tk.E+tk.S)
    make_resizable(3, 3, root)
    root.title("Tic Tac Toe, Player: " + turn)
    root.mainloop()


def main_menu():
    """
    Opens main menu
    """
    initialize_board()
    menu = tk.Tk()
    menu.geometry("250x138")
    menu.title("Tic Tac Toe")
    head = tk.Button(menu, text="---Welcome to tic-tac-toe---",
                     activeforeground='red',
                     activebackground="yellow", bg="red",
                     fg="yellow", width=500, font='summer', bd=5)

    play_as_o = tk.Button(menu, text="Play as o", command=lambda: play(menu, "O"),
                          activeforeground='red',
                          activebackground="yellow", bg="red",
                          fg="yellow", width=500, font='summer', bd=5)
    play_as_x = tk.Button(menu, text="Play as x", command=lambda: play(menu, "X"),
                          activeforeground='red',
                          activebackground="yellow", bg="red",
                          fg="yellow", width=500, font='summer', bd=5)
    head.pack(side='top')
    play_as_x.pack(side='top')
    play_as_o.pack(side='top')
    menu.mainloop()


# Call main function
if __name__ == '__main__':
    main_menu()
