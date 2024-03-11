# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest

from day19 import RobotCost, Blueprint, State

@pytest.fixture(name='example_blueprints')
def example_blueprints_fixture():
    return [
        Blueprint(
            blueprint_id = 1,
            ore_robot_cost = RobotCost(ore=4),
            clay_robot_cost = RobotCost(ore=2),
            obsidian_robot_cost = RobotCost(ore=3, clay=14),
            geode_robot_cost = RobotCost(ore=2, obsidian=7)
        ),
        Blueprint(
            blueprint_id = 2,
            ore_robot_cost = RobotCost(ore=2),
            clay_robot_cost = RobotCost(ore=3),
            obsidian_robot_cost = RobotCost(ore=3, clay=8),
            geode_robot_cost = RobotCost(ore=3, obsidian=12)
        )
    ]

@pytest.fixture(name='example_state')
def example_state_fixture(example_blueprints):
    return State(
        blueprint=example_blueprints[0], age=10,
        ore=100, clay=100, obsidian=100, geodes=100,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

def test_robot_cost():
    costs = (
        RobotCost(ore=4),
        RobotCost(ore=2),
        RobotCost(ore=3, clay=14),
        RobotCost(ore=2, obsidian=7)
    )

    assert (costs[0].ore, costs[0].clay, costs[0].obsidian) == (4, 0, 0)
    assert (costs[1].ore, costs[1].clay, costs[1].obsidian) == (2, 0, 0)
    assert (costs[2].ore, costs[2].clay, costs[2].obsidian) == (3, 14, 0)
    assert (costs[3].ore, costs[3].clay, costs[3].obsidian) == (2, 0, 7)


def test_blueprint():
    blueprint = Blueprint(
        blueprint_id = 1,
        ore_robot_cost = RobotCost(ore=4),
        clay_robot_cost = RobotCost(ore=2),
        obsidian_robot_cost = RobotCost(ore=3, clay=14),
        geode_robot_cost = RobotCost(ore=2, obsidian=7)
    )
    assert blueprint


def test_blueprint_from_string_spec(example_blueprints: list[Blueprint]):
    blueprint = Blueprint.from_string_spec('''
      Blueprint 1:
        Each ore robot costs 4 ore.
        Each clay robot costs 2 ore.
        Each obsidian robot costs 3 ore and 14 clay.
        Each geode robot costs 2 ore and 7 obsidian.
    ''')

    assert blueprint == example_blueprints[0]

def test_state(example_blueprints: list[Blueprint]):
    state = State(
        blueprint=example_blueprints[0],
        age=42,

        ore=1,
        clay=2,
        obsidian=3,
        geodes=4,

        ore_robots=5,
        clay_robots=6,
        obsidian_robots=7,
        geode_robots=8
    )

    assert state.blueprint == example_blueprints[0]
    assert state.age == 42
    assert (state.ore, state.clay, state.obsidian, state.geodes) == (1, 2, 3, 4)
    assert (
        state.ore_robots,
        state.clay_robots,
        state.obsidian_robots,
        state.geode_robots
    ) == (5, 6, 7, 8)

def test_state_basic(example_blueprints: list[Blueprint]):
    state = State(blueprint=example_blueprints[1])

    assert state.blueprint == example_blueprints[1]
    assert state.age == 0
    assert (state.ore, state.clay, state.obsidian, state.geodes) == (0, 0, 0, 0)
    assert (
        state.ore_robots,
        state.clay_robots,
        state.obsidian_robots,
        state.geode_robots
    ) == (1, 0, 0, 0)

def test_state_mine(example_state):

    example_state.mine()

    assert example_state == State(
        blueprint=example_state.blueprint, age=11,
        ore=105, clay=106, obsidian=107, geodes=108,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

def test_state_can_afford(example_blueprints: list[Blueprint]):

    state = State(
        blueprint=example_blueprints[0],
        ore=1,
        clay=2,
        obsidian=3,
        geodes=4,
    )
    affordable_cost = RobotCost(ore=1, obsidian=3)
    non_affordable_cost = RobotCost(ore=1, obsidian=30)
    assert state.can_afford(affordable_cost)
    assert not state.can_afford(non_affordable_cost)

def test_state_deduce_cost(example_state):

    state = example_state
    state.deduce_cost(RobotCost(ore=5, clay=5, obsidian=5))

    assert (state.ore, state.clay, state.obsidian) == (95, 95, 95)

def test_state_drop_excess(example_state):

    state = example_state
    state.drop_excess(10)

    assert (state.ore, state.clay, state.obsidian) == (40, 100, 70)

def test_state_next_states(example_state):

    next_states = example_state.next_states(False)

    assert next_states[0] == State(
        blueprint=example_state.blueprint, age=11,
        ore=103, clay=106, obsidian=100, geodes=108,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=9
    )

    assert next_states[1] == State(
        blueprint=example_state.blueprint, age=11,
        ore=105, clay=106, obsidian=107, geodes=108,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

    assert next_states[2] == State(
        blueprint=example_state.blueprint, age=11,
        ore=101, clay=106, obsidian=107, geodes=108,
        ore_robots=6, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

    assert next_states[3] == State(
        blueprint=example_state.blueprint, age=11,
        ore=103, clay=106, obsidian=107, geodes=108,
        ore_robots=5, clay_robots=7, obsidian_robots=7, geode_robots=8
    )

    assert next_states[4] == State(
        blueprint=example_state.blueprint, age=11,
        ore=102, clay=92, obsidian=107, geodes=108,
        ore_robots=5, clay_robots=6, obsidian_robots=8, geode_robots=8
    )



def test_state_next_states_poverty(example_blueprints):
    state = State(
        blueprint=example_blueprints[0], age=10,
        ore=1, clay=1, obsidian=1, geodes=1,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

    next_states = state.next_states()
    assert len(next_states) == 1

def test_state_next_states_optimized(example_blueprints):

    state = State(
        blueprint=example_blueprints[0], age=10,
        ore=100, clay=100, obsidian=0, geodes=100,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

    next_states = state.next_states()
    assert len(next_states) == 2

    assert next_states[0] == State(
        blueprint=state.blueprint, age=11,
        ore=105, clay=106, obsidian=7, geodes=108,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )
    assert next_states[1] == State(
        blueprint=state.blueprint, age=11,
        ore=103, clay=106, obsidian=7, geodes=108,
        ore_robots=5, clay_robots=7, obsidian_robots=7, geode_robots=8
    )

def test_state_next_states_super_optimized(example_blueprints):

    state = State(
        blueprint=example_blueprints[0], age=10,
        ore=100, clay=100, obsidian=100, geodes=100,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=8
    )

    next_states = state.next_states()
    assert len(next_states) == 1

    assert next_states[0] == State(
        blueprint=state.blueprint, age=11,
        ore=103, clay=106, obsidian=100, geodes=108,
        ore_robots=5, clay_robots=6, obsidian_robots=7, geode_robots=9
    )

def test_example_sequence(example_blueprints):
    state = State(blueprint=example_blueprints[0])

    state = state.just_mine()
    state = state.just_mine()
    state = state.build_clay_robot()
    state = state.just_mine()
    state = state.build_clay_robot()        # Minute 5
    state = state.just_mine()
    state = state.build_clay_robot()
    state = state.just_mine()
    state = state.just_mine()
    state = state.just_mine()               # Minute 10
    state = state.build_obsidian_robot()
    state = state.build_clay_robot()
    state = state.just_mine()
    state = state.just_mine()
    state = state.build_obsidian_robot()    # Minute 15
    state = state.just_mine()
    state = state.just_mine()
    state = state.build_geode_robot()
    state = state.just_mine()
    state = state.just_mine()               # Minute 20
    state = state.build_geode_robot()
    state = state.just_mine()
    state = state.just_mine()
    state = state.just_mine()

    assert state.ore == 6
    assert state.clay == 41
    assert state.obsidian == 8
    assert state.geodes == 9

    assert state.ore_robots == 1
    assert state.clay_robots == 4
    assert state.obsidian_robots == 2
    assert state.geode_robots == 2

def test_blueprint_max_geodes(example_blueprints):
    geodes = (
        example_blueprints[0].max_geodes(minutes=24),
        example_blueprints[1].max_geodes(minutes=24),
    )
    assert geodes == (9, 12)

def test_blueprint_max_geodes_longer(example_blueprints):
    pytest.skip('Takes too long (~2:20 mins)')
    geodes = (
        example_blueprints[0].max_geodes(minutes=32),
        example_blueprints[1].max_geodes(minutes=32),
    )
    assert geodes == (56, 62)
