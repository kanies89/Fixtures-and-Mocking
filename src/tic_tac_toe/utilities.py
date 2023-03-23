from functools import wraps

ALLOWED_SYMBOLS = 'X O'


def validate_board(function):
    @wraps(function)
    def wrapper(board):
        if not len(board) == 9:
            raise ValueError('improper board size')
        if not set(board) <= set(ALLOWED_SYMBOLS):
            raise ValueError('illegal symbol')
        return function(board)
    return wrapper


@validate_board
def tic_tac_toe_winner(board):
    for symbols in map(set, (
            *[board[n * 3:(n + 1) * 3] for n in range(3)],
            *[board[n::3] for n in range(3)],
            board[2:-1:2],
            board[::4]
    )):
        if len(symbols) == 1:
            if ' ' not in symbols:
                return symbols.pop()
