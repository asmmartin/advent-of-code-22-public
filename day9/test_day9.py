# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest

from day9 import Knot, Rope, Direction, parse_moves

@pytest.fixture
def example_input():
    return (
        'R 4\n'
        'U 4\n'
        'L 3\n'
        'D 1\n'
        'R 4\n'
        'D 1\n'
        'L 5\n'
        'R 2\n'
    )

@pytest.fixture
def example_larger_moves():
    return parse_moves(
        'R 5\n'
        'U 8\n'
        'L 8\n'
        'D 3\n'
        'R 17\n'
        'D 10\n'
        'L 25\n'
        'U 20\n'
    )

@pytest.fixture
def example_moves():
    return [
        Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT,
        Direction.UP, Direction.UP, Direction.UP, Direction.UP,
        Direction.LEFT, Direction.LEFT, Direction.LEFT,
        Direction.DOWN,
        Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT,
        Direction.RIGHT, Direction.RIGHT
    ]


def test_knot():
    assert Knot()
    assert Knot(x=2, y=4)
    assert Knot(x=1, y=1)

def test_default_rope():
    rope = Rope()
    assert rope.knots == (Knot(), Knot())

def test_rope():
    assert Rope(knots=(Knot(1, 2), Knot(2, 3)))

    with pytest.raises(ValueError):
        Rope(knots=(Knot(1, 2), Knot(2, 4)))

def test_directions():
    assert Direction.from_letter('U') == Direction.UP
    assert Direction.from_letter('D') == Direction.DOWN
    assert Direction.from_letter('L') == Direction.LEFT
    assert Direction.from_letter('R') == Direction.RIGHT

def test_parse_moves(example_input):
    moves = parse_moves(example_input)
    assert moves == [
        Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT,
        Direction.UP, Direction.UP, Direction.UP, Direction.UP,
        Direction.LEFT, Direction.LEFT, Direction.LEFT,
        Direction.DOWN,
        Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT,
        Direction.RIGHT, Direction.RIGHT
    ]

def test_rope_move_head_right_straight():
    rope = Rope((Knot(2, 1), Knot(1, 1)))
    rope.move_knot(Direction.RIGHT)
    assert rope.knots == (Knot(3, 1), Knot(2, 1))

def test_rope_move_head_down_straight():
    rope = Rope((Knot(1, 2), Knot(1, 3)))
    rope.move_knot(Direction.DOWN)
    assert rope.knots == (Knot(1, 1), Knot(1, 2))

def test_rope_move_head_up_diagonally():
    rope = Rope((Knot(2, 2), Knot(1, 1)))
    rope.move_knot(Direction.UP)
    assert rope.knots == (Knot(2, 3), Knot(2, 2))

def test_rope_move_head_right_diagonally():
    rope = Rope((Knot(2, 2), Knot(1, 1)))
    rope.move_knot(Direction.RIGHT)
    assert rope.knots == (Knot(3, 2), Knot(2, 2))

def test_multiple_moves(example_moves):
    rope = Rope()
    for move in example_moves:
        rope.move_knot(move)
    assert rope.knots == (Knot(2, 2), Knot(1, 2))
    assert len(rope.visited_by_tail) == 13

def test_long_rope_multiple_moves(example_moves):
    rope = Rope(tuple(Knot() for _ in range(10)))
    for move in example_moves:
        rope.move_knot(move)
    desired_knots = tuple((
        Knot(2, 2), Knot(1, 2), Knot(2, 2),
        Knot(3, 2), Knot(2, 2), Knot(1, 1),
        *(Knot() for _ in range(4))
    ))
    assert rope.knots == desired_knots

def test_long_rope_multiple_moves_large(example_larger_moves):
    rope = Rope(tuple(Knot() for _ in range(10)))
    for move in example_larger_moves:
        rope.move_knot(move)
    desired_knots = tuple(
        Knot(-11, 15 - offset) for offset in range(10)
    )
    assert rope.knots == desired_knots
    assert len(rope.visited_by_tail) == 36
