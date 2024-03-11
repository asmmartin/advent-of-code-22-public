# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest

from day24 import Blizzard, Movement, Valley, BlizzardsSimulator, find_path

@pytest.fixture(name='example_basic_valley')
def example_basic_valley_fixture():
    blizzards = frozenset((
        Blizzard(position=(2, 1), movement=Movement.EAST),
        Blizzard(position=(4, 4), movement=Movement.SOUTH)
    ))
    return Valley(dimensions=(7, 7), blizzards=blizzards)

@pytest.fixture(name='example_valley')
def example_valley_fixture():
    text = (
        "#.######\n"
        "#>>.<^<#\n"
        "#.<..<<#\n"
        "#>v.><>#\n"
        "#<^v^^>#\n"
        "######.#"
    )
    return Valley.from_string(text)

def test_blizzard():
    blizzard = Blizzard(position=(2, 1), movement=Movement.EAST)

    assert blizzard.position == (2, 1)
    assert blizzard.movement.value == (0, 1)

def test_valley():
    blizzards = frozenset((
        Blizzard(position=(2, 1), movement=Movement.EAST),
        Blizzard(position=(4, 4), movement=Movement.SOUTH)
    ))
    valley = Valley(
        dimensions=(7, 7), blizzards=blizzards,
    )

    assert valley.dimensions == (7, 7)
    assert valley.blizzards == blizzards
    assert valley.start_point == (0, 1) and valley.end_point == (6, 5)

def test_valley_from_string(example_basic_valley):
    basic_valley_text = (
        "#.#####\n"
        "#.....#\n"
        "#>....#\n"
        "#.....#\n"
        "#...v.#\n"
        "#.....#\n"
        "#####.#"
    )

    valley = Valley.from_string(basic_valley_text)

    assert valley == example_basic_valley

def test_blizzards_simulator(example_basic_valley):
    simulator = BlizzardsSimulator(starting_valley=example_basic_valley)

    assert simulator.get_valley(minute=0) == example_basic_valley

def test_blizzards_simulator_move_blizzards(example_basic_valley):
    simulator = BlizzardsSimulator(starting_valley=example_basic_valley)
    valley = example_basic_valley
    for _ in range(5):
        valley = simulator.move_blizzards(valley)
    assert valley == example_basic_valley

def test_blizzards_simulator_simulate_blizzards(example_basic_valley):

    simulator = BlizzardsSimulator(starting_valley=example_basic_valley)

    assert simulator.get_valley(minute=5) == example_basic_valley

def test_blizzards_simulator_simulate_blizzards_loop(example_basic_valley):
    simulator = BlizzardsSimulator(starting_valley=example_basic_valley)

    simulator.simulate_blizzards_until_loop()

    assert simulator.loop_length == 5
    assert id(simulator.get_valley(5)) == id(simulator.get_valley(0))
    assert id(simulator.get_valley(7)) == id(simulator.get_valley(2))

def test_valley_is_clear(example_basic_valley):

    assert example_basic_valley.is_clear((2, 5))
    assert example_basic_valley.is_clear((5, 1))
    assert example_basic_valley.is_clear((0, 1))
    assert example_basic_valley.is_clear((6, 5))

    assert not example_basic_valley.is_clear((0, 0))
    assert not example_basic_valley.is_clear((2, 1))
    assert not example_basic_valley.is_clear((4, 4))
    assert not example_basic_valley.is_clear((6, 3))

def test_find_path(example_valley):

    path = find_path(example_valley)

    assert len(path) - 1 == 18 # path includes the starting point too...

def test_find_path_with_precomputing(example_valley):

    simulator = BlizzardsSimulator(example_valley)
    simulator.simulate_blizzards_until_loop()

    path = find_path(example_valley, simulator)

    assert len(path) - 1 == 18 # path includes the starting point too...

def test_find_path_back_and_forth(example_valley):

    # Forward
    first_simulator = BlizzardsSimulator(example_valley)
    first_path = find_path(example_valley, first_simulator)
    assert len(first_path) - 1 == 18

    # Backward
    middle_valley = Valley(
        dimensions=example_valley.dimensions,
        start_point=example_valley.end_point,
        end_point=example_valley.start_point,
        blizzards=first_simulator.get_valley(len(first_path)-1).blizzards
    )
    middle_simulator = BlizzardsSimulator(middle_valley)
    middle_path = find_path(middle_valley, middle_simulator)
    assert len(middle_path) - 1 == 23

    # Forward again
    final_valley = Valley(
        dimensions=middle_valley.dimensions,
        start_point=middle_valley.end_point,
        end_point=middle_valley.start_point,
        blizzards=middle_simulator.get_valley(len(middle_path)-1).blizzards
    )
    final_simulator = BlizzardsSimulator(final_valley)
    final_path = find_path(final_valley, final_simulator)
    assert len(final_path) - 1 == 13
