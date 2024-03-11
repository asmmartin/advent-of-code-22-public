# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest
from day22 import parse_instructions, DIRECTIONS, Board


@pytest.fixture(name='example_board_text')
def example_board_text_fixture():
    return (
        "        ...#\n"
        "        .#..\n"
        "        #...\n"
        "        ....\n"
        "...#.......#\n"
        "........#...\n"
        "..#....#....\n"
        "..........#.\n"
        "        ...#....\n"
        "        .....#..\n"
        "        .#......\n"
        "        ......#.\n"
    )

@pytest.fixture(name='example_board')
def example_board_fixture(example_board_text):
    return Board(example_board_text)

def test_parse_instructions():
    instructions_text = "10R5L5R10L4R5L5"

    instructions = parse_instructions(instructions_text)

    assert instructions == [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]

def test_directions():
    assert DIRECTIONS == [
        (0, 1, '>'),
        (1, 0, 'v'),
        (0, -1, '<'),
        (-1, 0, '^')
    ]

def test_board(example_board_text):
    board = Board(layout=example_board_text)

    assert board.current_tile_coords == (0, 8)
    assert board.current_direction_index == 0
    assert board.width == 16
    assert board.height == 12

def test_board_next_tile_normal(example_board):

    example_board.current_tile_coords = (2, 10)

    example_board.current_direction_index = 0
    assert example_board.next_tile_coords == (2, 11)

    example_board.current_direction_index = 1
    assert example_board.next_tile_coords == (3, 10)

    example_board.current_direction_index = 2
    assert example_board.next_tile_coords == (2, 9)

    example_board.current_direction_index = 3
    assert example_board.next_tile_coords == (1, 10)

def test_board_next_tile_wrapping(example_board):

    example_board.current_tile_coords = (6, 11)
    example_board.current_direction_index = 0
    assert example_board.next_tile_coords == (6, 0)

    example_board.current_tile_coords = (6, 0)
    example_board.current_direction_index = 2
    assert example_board.next_tile_coords == (6, 11)

    example_board.current_tile_coords = (7, 5)
    example_board.current_direction_index = 1
    assert example_board.next_tile_coords == (4, 5)

    example_board.current_tile_coords = (4, 5)
    example_board.current_direction_index = 3
    assert example_board.next_tile_coords == (7, 5)

def test_board_example_path(example_board):

    instructions = [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]

    for instruction in instructions:
        example_board.apply_instruction(instruction)

    assert example_board.current_tile_coords == (5, 7)
    assert example_board.password == 6032

def test_board_next_tile_wrapping_cube(example_board):

    example_board.edges = {}

    example_board.edges.update({(0, 8+i, 3): (4, 3-i, 1) for i in range(4)})
    example_board.edges.update({(0+i, 8, 2): (4, 4+i, 1) for i in range(4)})
    example_board.edges.update({(0+i, 11, 0): (11-i, 15, 2) for i in range(4)})
    example_board.edges.update({(4+i, 11, 0): (8, 15-i, 1) for i in range(4)})
    example_board.edges.update({(7, 4+i, 1): (11-i, 8, 0) for i in range(4)})
    example_board.edges.update({(7, i, 1): (11, 11-i, 3) for i in range(4)})
    example_board.edges.update({(4+i, 0, 2): (11, 15-i, 3) for i in range(4)})

    reverse_edges = {}
    for k, v in example_board.edges.items():
        reverse_edges[(v[0], v[1], (v[2] + 2) % 4)] = (k[0], k[1], (k[2] + 2) % 4)
    example_board.edges.update(reverse_edges)

    A = (5, 11)
    B = (8, 14)
    C = (11, 10)
    D = (7, 1)

    example_board.current_direction_index = 0
    example_board.current_tile_coords = A
    assert example_board.next_tile_coords == B
    assert example_board.next_direction_index == 1

    example_board.current_direction_index = 3
    example_board.current_tile_coords = B
    assert example_board.next_tile_coords == A
    assert example_board.next_direction_index == 2

    example_board.current_direction_index = 1
    example_board.current_tile_coords = C
    assert example_board.next_tile_coords == D
    assert example_board.next_direction_index == 3

    example_board.current_direction_index = 1
    example_board.current_tile_coords = D
    assert example_board.next_tile_coords == C
    assert example_board.next_direction_index == 3

def test_board_example_path_cube(example_board):

    instructions = [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]

    example_board.edges = {}

    example_board.edges.update({(0, 8+i, 3): (4, 3-i, 1) for i in range(4)})
    example_board.edges.update({(0+i, 8, 2): (4, 4+i, 1) for i in range(4)})
    example_board.edges.update({(0+i, 11, 0): (11-i, 15, 2) for i in range(4)})
    example_board.edges.update({(4+i, 11, 0): (8, 15-i, 1) for i in range(4)})
    example_board.edges.update({(7, 4+i, 1): (11-i, 8, 0) for i in range(4)})
    example_board.edges.update({(7, i, 1): (11, 11-i, 3) for i in range(4)})
    example_board.edges.update({(4+i, 0, 2): (11, 15-i, 3) for i in range(4)})

    reverse_edges = {}
    for k, v in example_board.edges.items():
        reverse_edges[(v[0], v[1], (v[2] + 2) % 4)] = (k[0], k[1], (k[2] + 2) % 4)
    example_board.edges.update(reverse_edges)

    for instruction in instructions:
        example_board.apply_instruction(instruction)

    assert example_board.current_tile_coords == (4, 6)
    assert example_board.password == 5031
