from src.tic_tac_toe.utilities import tic_tac_toe_winner
from src.tic_tac_toe.api import app

from os import close, unlink
from tempfile import mkstemp
from itertools import count
from sqlalchemy import create_engine
from unittest import TestCase

from src.tic_tac_toe.database import winner, metadata, history
import pytest
import unittest


@pytest.fixture
def create_games(database_connection):
    def game_creator(*games):
        move_id = count(1)
        for game_id, moves in enumerate(games, 1):
            database_connection.execute(history.insert(), [
                {
                    'game_id': game_id,
                    'move_id': next(move_id),
                    'position': int(position),
                    'symbol': symbol
                } for position, symbol in zip(moves[::2], moves[1::2])
            ])

    return game_creator


@pytest.fixture
def database_connection():
    fd, name = mkstemp(prefix='test_winner_', suffix='.sqlite')
    engine = create_engine(f'sqlite:///{name}')
    metadata.create_all(engine)
    with engine.connect() as connection:
        yield connection
    close(fd)
    unlink(name)


def test_3x_in_a_column(database_connection):
    assert winner(database_connection, 1) == 'X'


class TestWinner(TestCase):
    games = [
        '4X1O5X3O2X6O8X'
    ]

    def setUp(self):
        self.fd, self.name = mkstemp(prefix='test_winner_', suffix='.sqlite')  # ➜ 1
        engine = create_engine(f'sqlite:///{self.name}')
        metadata.create_all(engine)  # ➜ 2

        move_id = count(1)

        with engine.connect() as connection:
            for game_id, moves in enumerate(self.games, 1):  # ➜ 3
                connection.execute(history.insert(), [
                    {
                        'game_id': game_id,
                        'move_id': next(move_id),
                        'position': int(position),
                        'symbol': symbol
                    } for position, symbol in zip(moves[::2], moves[1::2])
                ])

        self.connection = engine.connect()


# tests/test_winner_api.py
def test_api_missing_parameter():
    assert app.test_client().get('/winner').status_code == 400


def test_api_is_wsgi_app():
    assert hasattr(app, 'wsgi_app')


class TestFinishedGame(unittest.TestCase):

    def test_3x_in_a_row(self):
        for i, board in enumerate(('XXXO  O O', 'O  XXXO O', 'O OO  XXX')):
            with self.subTest(row=i + 1):
                self.assertEqual(tic_tac_toe_winner(board), 'X')

    # kolejne testy dla planszy opisujących zakończone gry


class TestUnfinishedGame(unittest.TestCase):

    def test_empty_board(self):
        self.assertIsNone(tic_tac_toe_winner(' ' * 9))

    # kolejne testy dla niezakończonych gier


class TestInvalidBoard(unittest.TestCase):

    def test_illegal_symbols(self):
        with self.assertRaises(ValueError):
            tic_tac_toe_winner('    E    ')

    # kolejne testy nieprawidłowego wejścia


class SkipTest(unittest.TestCase):

    @unittest.skip('not implemented')
    def test_3x_in_a_column(self):
        self.assertEqual(tic_tac_toe_winner('X  XO XOO'), 'X')


def test_api_3x_in_a_row():
    response = app.test_client().get('/winner?board=XXX_O_O__')
    assert response.status_code == 200 and response.json['winner'] == 'X'


def test_api_unfinished_game():
    response = app.test_client().get('/winner?board=X_____O__')
    assert response.status_code == 200 and response.json['winner'] is None
