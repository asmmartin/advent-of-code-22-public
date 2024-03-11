# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest
import day17


SAMPLE_JETS_PATTERN = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
SAMPLE_ROCKS_AFTER_ROTATION = {
    (2+0j), (3+0j), (4+0j), (5+0j), (2+2j), (3+2j), (4+2j), (2+4j), (4+4j),
    (4+6j), (4+8j), (5+8j), (2+10j), 12j, (1+12j), (2+12j), (3+12j), (4+12j),
    (5+12j), (4+14j), (5+14j), (4+16j), (3+1j), 3j, (1+3j), (2+3j), (3+3j),
    (4+3j), (2+5j), (4+5j), (4+7j), (5+7j), (1+9j), (2+9j), (3+9j), (4+9j),
    (1+11j), (2+11j), (3+11j), 13j, (1+13j), (4+13j), (5+13j), (4+15j)
}

@pytest.fixture
def example_chamber():
    return day17.Chamber(SAMPLE_JETS_PATTERN)

def test_jets_generator():
    jets_gen = day17.jets_generator(pattern=SAMPLE_JETS_PATTERN)
    for _ in range(83):
        next(jets_gen)

    assert [next(jets_gen)[1] for _ in range(10)] == [
        -1, -1, 1, -1, 1, 1, -1, -1, -1, 1
    ]

def test_rocks_generator():
    rocks_gen = day17.rocks_generator()

    rocks = [next(rocks_gen)[1] for _ in range(10)]

    assert rocks == [
        {0, 1, 2, 3},
        {1, 1j, 1+1j, 2+1j, 1+2j},
        {0, 1, 2, 2+1j, 2+2j},
        {0, 1j, 2j, 3j},
        {0, 1, 1j, 1+1j}
    ]*2

def test_chamber(example_chamber):
    chamber = example_chamber

    assert chamber.rocks == set()
    assert chamber.rocks_height == -1
    assert chamber.current_rock is None
    assert chamber.jets_gen
    assert chamber.rocks_gen
    assert chamber.WIDTH == 7

def test_chamber_start_rock(example_chamber):
    chamber = example_chamber

    chamber.start_rock(next(chamber.rocks_gen)[1])
    assert chamber.current_rock == {x + 3j for x in [2, 3, 4, 5]}

    chamber.rocks = {2, 3, 4, 5}
    chamber.rocks_height = 1
    chamber.start_rock(next(chamber.rocks_gen)[1])
    assert chamber.current_rock == {
        3+5j, 2+6j, 3+6j, 4+6j, 3+7j
    }

def test_chamber_rock_move(example_chamber):
    chamber = example_chamber

    chamber.rocks = {2, 2+1j, 2+2j, 2+3j}

    # Move left
    chamber.current_rock = {tile + (1+10j) for tile in day17.ROCKS[1]}
    assert chamber.move_rock(direction=-1)
    assert chamber.current_rock == {tile + (10j) for tile in day17.ROCKS[1]}

    # Move right
    chamber.current_rock = {tile + (1+10j) for tile in day17.ROCKS[1]}
    assert chamber.move_rock(direction=1)
    assert chamber.current_rock == {tile + (2+10j) for tile in day17.ROCKS[1]}

    # Move left through wall
    chamber.current_rock = {tile + (7j) for tile in day17.ROCKS[4]}
    assert not chamber.move_rock(direction=-1)
    assert chamber.current_rock == {tile + (7j) for tile in day17.ROCKS[4]}

    # Move right through wall
    chamber.current_rock = {tile + (3+7j) for tile in day17.ROCKS[0]}
    assert not chamber.move_rock(direction=1)
    assert chamber.current_rock == {tile + (3+7j) for tile in day17.ROCKS[0]}

    # Move left through rock
    chamber.current_rock = {tile + (3+1j) for tile in day17.ROCKS[2]}
    assert not chamber.move_rock(direction=-1)
    assert chamber.current_rock == {tile + (3+1j) for tile in day17.ROCKS[2]}

    # Move right through rock
    chamber.current_rock = {tile + (3j) for tile in day17.ROCKS[1]}
    assert not chamber.move_rock(direction=1)
    assert chamber.current_rock == {tile + (3j) for tile in day17.ROCKS[1]}

    # Move down
    chamber.current_rock = {tile + (1j) for tile in day17.ROCKS[3]}
    assert chamber.move_rock(direction=-1j)
    assert chamber.current_rock == day17.ROCKS[3]

    # Move down through floor
    chamber.current_rock = day17.ROCKS[3]
    assert not chamber.move_rock(direction=-1j)
    assert chamber.current_rock == day17.ROCKS[3]

    # Move down through rock
    chamber.current_rock = {tile + (3j) for tile in day17.ROCKS[1]}
    assert not chamber.move_rock(direction=-1j)
    assert chamber.current_rock == {tile + (3j) for tile in day17.ROCKS[1]}

def test_chamber_drop_rock(example_chamber):
    chamber = example_chamber

    chamber.drop_rock()
    assert chamber.rocks == {
        2, 3, 4, 5
    }

    chamber.drop_rock()
    assert chamber.rocks == {
        2, 3, 4, 5, 3+1j, 2+2j, 3+2j, 4+2j, 3+3j
    }

    for _ in range(8):
        chamber.drop_rock()

    assert chamber.rocks == SAMPLE_ROCKS_AFTER_ROTATION

def test_part_1_example():
    chamber = day17.Chamber(SAMPLE_JETS_PATTERN)
    for _ in range(2022):
        chamber.drop_rock()

    assert chamber.rocks_height + 1 == 3068

def test_chamber_remove_non_relevant_rocks(example_chamber):
    chamber = example_chamber
    for _ in range(10):
        chamber.drop_rock()

    chamber.rocks.add(6+12j)
    chamber.remove_non_relevant_rocks()
    assert chamber.rocks == {
        13j, 1+13j, 2+12j, 3+12j, 4+13j,
        4+14j, 4+15j, 4+16j, 5+13j, 5+14j, 6+12j
    }

def test_normalize_rock_tiles():
    rock_tiles = {13j, 1+13j, 2+12j, 3+12j, 4+13j,
        4+14j, 4+15j, 4+16j, 5+13j, 5+14j, 6+12j}

    normalized = day17.normalize_rock_tiles(rock_tiles)

    assert normalized == {
        1j, 1+1j, 2, 3, 4+1j,
        4+2j, 4+3j, 4+4j, 5+1j, 5+2j, 6
    }
