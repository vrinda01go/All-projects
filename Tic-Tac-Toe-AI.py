import tkinter as tk
from collections import Counter

BOARD_EMPTY = 0
BOARD_PLAYER_X = 1
BOARD_PLAYER_O = -1

def player(s):
    counter = Counter(s)
    x_places = counter[1]
    o_places = counter[-1]

    if x_places + o_places == 9:
        return None
    elif x_places > o_places:
        return BOARD_PLAYER_O 
    else:
        return BOARD_PLAYER_X

def actions(s):
    play = player(s)
    actions_list = [(play, i) for i in range(len(s)) if s[i] == BOARD_EMPTY]
    return actions_list

def result(s, a):
    (play, index) = a
    s_copy = s.copy()
    s_copy[index] = play
    return s_copy

def terminal(s):
    for i in range(3):
        if s[3 * i] == s[3 * i + 1] == s[3 * i + 2] != BOARD_EMPTY:
            return s[3 * i]
        if s[i] == s[i + 3] == s[i + 6] != BOARD_EMPTY:
            return s[i]

    if s[0] == s[4] == s[8] != BOARD_EMPTY:
        return s[0]
    if s[2] == s[4] == s[6] != BOARD_EMPTY:
        return s[2]

    if player(s) is None:
        return 0
    
    return None

def utility(s, cost):
    term = terminal(s)
    if term is not None:
        return (term, cost)
    
    action_list = actions(s)
    utils = []
    for action in action_list:
        new_s = result(s, action)
        utils.append(utility(new_s, cost + 1))

    score = utils[0][0]
    idx_cost = utils[0][1]
    play = player(s)
    if play == BOARD_PLAYER_X:
        for i in range(len(utils)):
           if utils[i][0] > score:
                score = utils[i][0]
                idx_cost = utils[i][1]
    else:
        for i in range(len(utils)):
           if utils[i][0] < score:
                score = utils[i][0]
                idx_cost = utils[i][1]
    return (score, idx_cost) 

def minimax(s):
    action_list = actions(s)
    utils = []
    for action in action_list:
        new_s = result(s, action)
        utils.append((action, utility(new_s, 1)))

    if len(utils) == 0:
        return ((0,0), (0, 0))

    sorted_list = sorted(utils, key=lambda l : l[0][1])
    action = min(sorted_list, key = lambda l : l[1])
    return action

def print_board(s, buttons):
    def convert(num):
        if num == BOARD_PLAYER_X:
            return 'X'
        if num == BOARD_PLAYER_O:
            return 'O'
        return '_'

    for i in range(9):
        buttons[i].config(text=convert(s[i]))

def on_click(index):
    global s
    if terminal(s) is None and s[index] == BOARD_EMPTY:
        s = result(s, (BOARD_PLAYER_X, index))
        print_board(s, buttons)
        if terminal(s) is None:
            action = minimax(s)
            s = result(s, action[0])
            print_board(s, buttons)
    if terminal(s) is not None:
        if terminal(s) == BOARD_PLAYER_X:
            result_label.config(text="You have won!")
        elif terminal(s) == BOARD_PLAYER_O:
            result_label.config(text="You have lost!")
        else:
            result_label.config(text="It's a tie.")

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")

s = [BOARD_EMPTY for _ in range(9)]

buttons = [tk.Button(root, text='_', font=('Arial', 24), width=5, height=2,
                     command=lambda i=i: on_click(i)) for i in range(9)]

for i in range(3):
    for j in range(3):
        buttons[i*3 + j].grid(row=i, column=j)

result_label = tk.Label(root, text="", font=('Arial', 16))
result_label.grid(row=3, column=0, columnspan=3)

root.mainloop()
