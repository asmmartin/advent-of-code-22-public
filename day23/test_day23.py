# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest

from day23 import Groove

@pytest.fixture(name='simple_example_groove_text')
def simple_example_groove_text_fixture():
    return (
        ".....\n"
        "..##.\n"
        "..#..\n"
        ".....\n"
        "..##.\n"
        "....."
    )

@pytest.fixture(name='example_groove_text')
def example_groove_text_fixture():
    return (
        "....#..\n"
        "..###.#\n"
        "#...#.#\n"
        ".#...##\n"
        "#.###..\n"
        "##.#.##\n"
        ".#..#.."
    )

@pytest.fixture(name='example_groove')
def example_groove_fixture():

    elves = {
                                        (0, 4),
                        (1, 2), (1, 3), (1, 4),         (1, 6),
        (2, 0),                         (2, 4),         (2, 6),
                (3, 1),                         (3, 5), (3, 6),
        (4, 0),         (4, 2), (4, 3), (4, 4),
        (5, 0), (5, 1),         (5, 3),         (5, 5), (5, 6),
                (6, 1),                 (6, 4)

    }
    return Groove(elves=elves)

@pytest.fixture(name='simple_example_groove')
def simple_example_groove_fixture(simple_example_groove_text):

    return Groove.from_text(simple_example_groove_text)

def test_groove():

    elves = {
                                        (0, 4),
                        (1, 2), (1, 3), (1, 4),         (1, 6),
        (2, 0),                         (2, 4),         (2, 6),
                (3, 1),                         (3, 5), (3, 6),
        (4, 0),         (4, 2), (4, 3), (4, 4),
        (5, 0), (5, 1),         (5, 3),         (5, 5), (5, 6),
                (6, 1),                 (6, 4)

    }
    groove = Groove(elves=elves)

    assert len(groove.elves) == 22

def test_groove_from_text(example_groove_text):

    elves = {
                                        (0, 4),
                        (1, 2), (1, 3), (1, 4),         (1, 6),
        (2, 0),                         (2, 4),         (2, 6),
                (3, 1),                         (3, 5), (3, 6),
        (4, 0),         (4, 2), (4, 3), (4, 4),
        (5, 0), (5, 1),         (5, 3),         (5, 5), (5, 6),
                (6, 1),                 (6, 4)

    }
    groove = Groove.from_text(example_groove_text)

    assert groove.elves == elves

def test_groove_check_north_is_empty(example_groove):

    assert example_groove.check_north_is_empty((0, 4))
    assert example_groove.check_north_is_empty((2, 0))
    assert example_groove.check_north_is_empty((4, 3))

    assert example_groove.check_north_is_empty((1, 4)) == (0, 0)
    assert example_groove.check_north_is_empty((4, 4)) == (0, 0)
    assert example_groove.check_north_is_empty((5, 5)) == (0, 0)

def test_groove_check_south_is_empty(example_groove):

    assert example_groove.check_south_is_empty((1, 2))
    assert example_groove.check_south_is_empty((5, 6))
    assert example_groove.check_south_is_empty((6, 1))

    assert example_groove.check_south_is_empty((1, 4)) == (0, 0)
    assert example_groove.check_south_is_empty((4, 4)) == (0, 0)
    assert example_groove.check_south_is_empty((5, 0)) == (0, 0)

def test_groove_check_east_is_empty(example_groove):

    assert example_groove.check_east_is_empty((0, 4))
    assert example_groove.check_east_is_empty((1, 6))
    assert example_groove.check_east_is_empty((6, 1))

    assert example_groove.check_east_is_empty((1, 3)) == (0, 0)
    assert example_groove.check_east_is_empty((4, 4)) == (0, 0)
    assert example_groove.check_east_is_empty((5, 3)) == (0, 0)

def test_groove_check_west_is_empty(example_groove):

    assert example_groove.check_west_is_empty((1, 2))
    assert example_groove.check_west_is_empty((1, 6))
    assert example_groove.check_west_is_empty((2, 0))

    assert example_groove.check_west_is_empty((1, 3)) == (0, 0)
    assert example_groove.check_west_is_empty((2, 6)) == (0, 0)
    assert example_groove.check_west_is_empty((4, 4)) == (0, 0)

def test_groove_check_functions(example_groove):

    assert example_groove.check_functions == [
        example_groove.check_north_is_empty,
        example_groove.check_south_is_empty,
        example_groove.check_west_is_empty,
        example_groove.check_east_is_empty,
    ]

def test_groove_rotate_check_functions(example_groove):

    example_groove.rotate_check_functions()
    example_groove.rotate_check_functions()

    assert example_groove.check_functions == [
        example_groove.check_west_is_empty,
        example_groove.check_east_is_empty,
        example_groove.check_north_is_empty,
        example_groove.check_south_is_empty,
    ]

def test_groove_propose_elves(simple_example_groove):

    proposed = simple_example_groove.propose_elves()

    assert proposed == {
        (1, 2): (0, 2),
        (1, 3): (0, 3),
        (2, 2): (3, 2),
        (4, 2): (3, 2),
        (4, 3): (3, 3)
    }

def test_groove_round(simple_example_groove):

    simple_example_groove.round()

    assert simple_example_groove.elves == {
        (0, 2),
        (0, 3),
        (2, 2),
        (4, 2),
        (3, 3)
    }
def test_groove_round_simple_ten_times(simple_example_groove):

    for _ in range(10):
        simple_example_groove.round()

    assert simple_example_groove.elves == {
        (0, 2),
        (1, 4),
        (2, 0),
        (3, 4),
        (5, 2)
    }

def test_groove_soil(simple_example_groove):

    assert simple_example_groove.soil == 3

    for _ in range(10):
        simple_example_groove.round()

    assert simple_example_groove.soil == 25

def test_groove_soil_complex(example_groove):

    for _ in range(10):
        example_groove.round()

    assert example_groove.soil == 110

def test_groove_go_until_still(simple_example_groove, example_groove):

    simple_rounds = simple_example_groove.go_until_still()
    complex_rounds = example_groove.go_until_still()

    assert simple_rounds == 4
    assert complex_rounds == 20
