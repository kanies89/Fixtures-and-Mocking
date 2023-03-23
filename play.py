import random
from src.tic_tac_toe.utilities import tic_tac_toe_winner

board = "         "
chosen = [0, 1, 2, 3, 4, 5, 6, 7, 8]


while " " in board:
    x_mark = chosen.pop(random.randint(0, len(chosen) - 1))
    board = board[:x_mark] + "X" + board[x_mark + 1:]
    if len(chosen) == 0:
        break
    y_mark = chosen.pop(random.randint(0, len(chosen) - 1))
    board = board[:y_mark] + "O" + board[y_mark + 1:]
    winner = tic_tac_toe_winner(board)
    if winner is not None:
        print(f'{winner} won!')
        break

if winner is None:
    print("Tie!")

