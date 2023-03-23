# tic_tac_toe/database.py
from sqlalchemy import Table, Column, Integer, String, MetaData, select

from .utilities import tic_tac_toe_winner
import requests

metadata = MetaData()

history = Table(
    'history',
    metadata,
    Column('game_id', Integer, nullable=False),
    Column('move_id', Integer, primary_key=True),
    Column('position', Integer, nullable=False),
    Column('symbol', String(1), nullable=False)
)


def winner(connection, game_id):
    metadata.create_all(connection)
    query = select([history.c.position, history.c.symbol]) \
        .where(history.c.game_id == game_id) \
        .order_by(history.c.move_id.asc())
    board = {position: symbol for position, symbol in connection.execute(query)}
    return requests.get('http://127.0.0.1:5000/winner', params={
        'board': ''.join(board.get(position, ' ') for position in range(9))
    })