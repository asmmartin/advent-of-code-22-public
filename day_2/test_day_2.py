# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-name-in-module
# pylint: disable=redefined-outer-name

from unittest import mock
import pytest

import day_2

@pytest.fixture
def example_strategy():
    game_reprs = ['A Y', 'B X', 'C Z']
    return [day_2.Game(game_repr) for game_repr in game_reprs]

def test_parse_strategy():

    with mock.patch('day_2.read_input_lines') as read_mock:
        read_mock.return_value = ['A Y', 'B X', 'C Z']

        strategy = day_2.parse_strategy('day_2/input.txt')

    assert strategy[0].opponent == day_2.Shape.ROCK
    assert strategy[0].mine == day_2.Shape.ROCK

    assert strategy[1].opponent == day_2.Shape.PAPER
    assert strategy[1].mine == day_2.Shape.ROCK

    assert strategy[2].opponent == day_2.Shape.SCISSORS
    assert strategy[2].mine == day_2.Shape.ROCK


def test_shape_from_str():

    assert day_2.Shape.from_str_one('A') == day_2.Shape.ROCK
    assert day_2.Shape.from_str_one('B') == day_2.Shape.PAPER
    assert day_2.Shape.from_str_one('C') == day_2.Shape.SCISSORS
    assert day_2.Shape.from_str_one('X') == day_2.Shape.ROCK
    assert day_2.Shape.from_str_one('Y') == day_2.Shape.PAPER
    assert day_2.Shape.from_str_one('Z') == day_2.Shape.SCISSORS

def test_calculate_game_score_(example_strategy):
    assert example_strategy[0].score == 4
    assert example_strategy[1].score == 1
    assert example_strategy[2].score == 7

def test_total_score(example_strategy):
    total_score = sum(game.score for game in example_strategy)
    assert total_score == 12
