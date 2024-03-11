# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

from unittest import mock
import day12

SAMPLE_GRID = [
    'Sabqponm',
    'abcryxxl',
    'accszExk',
    'acctuvwj',
    'abdefghi'
]

def test_find_extremes():
    start, end = day12.find_extremes(SAMPLE_GRID)
    assert start == (0, 0)
    assert end == (2, 5)

def test_find_extremes_non_default():
    start, end = day12.find_extremes(SAMPLE_GRID, 'E', None)
    assert start == (2, 5)
    assert end is None

def test_calculate_height():
    assert day12.calculate_height('a') == 0
    assert day12.calculate_height('z') == 25
    assert day12.calculate_height('S') == 0
    assert day12.calculate_height('E') == 25

def test_get_valid_neighbours():
    assert day12.get_valid_neighbours(SAMPLE_GRID, (0, 0)) == [(1, 0), (0, 1)]
    assert day12.get_valid_neighbours(SAMPLE_GRID, (2, 1)) == [
        (3, 1), (2, 2), (1, 1), (2, 0)
    ]

@mock.patch('day12.find_extremes', return_value=((0, 0), (2, 5)))
def test_path_to_top(_):
    _, steps = day12.path_to_top(SAMPLE_GRID)
    assert len(steps) == 31

@mock.patch('day12.find_extremes', return_value=((2, 5), None))
def test_path_to_top_hicking(_):
    _, steps = day12.path_to_top(SAMPLE_GRID, True)
    assert len(steps) == 29

def test_calculate_step():
    assert day12.calculate_step((3, 7), (2, 7)) == '^'
    assert day12.calculate_step((3, 7), (4, 7)) == 'v'
    assert day12.calculate_step((3, 7), (3, 6)) == '<'
    assert day12.calculate_step((3, 7), (3, 8)) == '>'

def test_draw_path():
    steps = [
        (0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (4, 4),
        (4, 5), (4, 6), (4, 7), (3, 7), (2, 7), (1, 7), (0, 7), (0, 6), (0, 5),
        (0, 4), (0, 3), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (3, 6), (2, 6),
        (1, 6), (1, 5), (1, 4), (2, 4)
    ]

    end_tile = (2, 5)
    dimensions = (5, 8)

    drawn_path = day12.draw_path(dimensions, steps, end_tile)

    assert drawn_path == (
        'v..v<<<<\n'
        '>v.vv<<^\n'
        '.v.v>E^^\n'
        '.>v>>>^^\n'
        '..>>>>>^'
    )
