import pytest

from src.tic_tac_toe.utilities import tic_tac_toe_winner


def test_3x_diagonally():
    assert tic_tac_toe_winner('XO OX   X') == 'X'


def test_too_large_board():
    with pytest.raises(ValueError):
        tic_tac_toe_winner('XOOOXXXXOX')
