# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import copy
import re
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Self

@dataclass(frozen=True)
class RobotCost:
    ore: int
    clay: int = 0
    obsidian: int = 0

@dataclass(unsafe_hash=True)
class Blueprint:
    blueprint_id: int
    ore_robot_cost: RobotCost
    clay_robot_cost:  RobotCost
    obsidian_robot_cost: RobotCost
    geode_robot_cost: RobotCost

    def __post_init__(self):
        self.max_ore_cost = max((
            self.ore_robot_cost.ore, self.clay_robot_cost.ore,
            self.obsidian_robot_cost.ore, self.geode_robot_cost.ore
        ))
        self.max_clay_cost = max((
            self.ore_robot_cost.clay, self.clay_robot_cost.clay,
            self.obsidian_robot_cost.clay, self.geode_robot_cost.clay
        ))
        self.max_obsidian_cost = max((
            self.ore_robot_cost.obsidian, self.clay_robot_cost.obsidian,
            self.obsidian_robot_cost.obsidian, self.geode_robot_cost.obsidian
        ))

    @classmethod
    def from_string_spec(cls, spec: str) -> Self:
        blueprint_id = re.search(r'Blueprint (\d+)', spec)
        ore = re.search(r'Each ore robot costs (\d+) ore.', spec)
        clay = re.search(r'Each clay robot costs (\d+) ore.', spec)
        obsidian = re.search(r'Each obsidian robot costs (\d+) ore and (\d+) clay.', spec)
        geode = re.search(r'Each geode robot costs (\d+) ore and (\d+) obsidian.', spec)

        if not all((blueprint_id, ore, clay, obsidian, geode)):
            raise ValueError('Invalid string spec!:', spec)

        # Note: Disabling linter in next lines, previous check guards for Nones
        return Blueprint(
            blueprint_id=int(blueprint_id.group(1)), # type: ignore
            ore_robot_cost=RobotCost(ore=int(ore.group(1))), # type: ignore
            clay_robot_cost=RobotCost(ore=int(clay.group(1))), # type: ignore
            obsidian_robot_cost=RobotCost(
                ore=int(obsidian.group(1)), clay=int(obsidian.group(2)) # type: ignore
            ),
            geode_robot_cost=RobotCost(
                ore=int(geode.group(1)), obsidian=int(geode.group(2)) # type: ignore
            )
        )

    def max_geodes(self, minutes: int) -> int:

        def potential_geodes(state: 'State') -> int:
            remaining = minutes - state.age
            return (
                state.geodes +
                remaining * state.geode_robots +
                int(remaining * (remaining - 1) / 2)
            )

        base_state = State(blueprint=self)
        states_to_process = deque([base_state])
        already_processed = set()
        max_geodes = 0

        while states_to_process:
            state = states_to_process.pop()

            if state in already_processed:
                continue
            already_processed.add(state)

            if potential_geodes(state) <= max_geodes:
                continue

            if state.age == minutes:
                max_geodes = max(state.geodes, max_geodes)
                continue
            states_to_process.extend([
                state.drop_excess(minutes - state.age)
                for state in state.next_states()
            ])

        return max_geodes

@dataclass(unsafe_hash=True)
class State:
    blueprint: Blueprint
    age: int = 0

    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

    ore_robots: int = 1
    clay_robots: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0

    def can_afford(self, cost: RobotCost) -> bool:
        return all((
            self.ore >= cost.ore,
            self.clay >= cost.clay,
            self.obsidian >= cost.obsidian
        ))

    def mine(self) -> Self:
        self.age += 1
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes += self.geode_robots

        return self

    def deduce_cost(self, cost: RobotCost):
        self.ore -= cost.ore
        self.clay -= cost.clay
        self.obsidian -= cost.obsidian

    def drop_excess(self, remaining: int) -> Self:
        max_needed_ore = remaining * self.blueprint.max_ore_cost
        max_needed_clay = remaining * self.blueprint.max_clay_cost
        max_needed_obsidian = remaining * self.blueprint.max_obsidian_cost

        self.ore = min(self.ore, max_needed_ore)
        self.clay = min(self.clay, max_needed_clay)
        self.obsidian = min(self.obsidian, max_needed_obsidian)

        return self

    def next_states(self, optimized: bool = True) -> list[Self]:

        next_states = []
        if (new_state := self.build_geode_robot()):
            next_states.append(new_state)
            if optimized:
                return next_states

        new_state = self.just_mine()
        next_states.append(new_state)


        if (new_state := self.build_ore_robot(optimized)):
            next_states.append(new_state)
        if (new_state := self.build_clay_robot(optimized)):
            next_states.append(new_state)
        if (new_state := self.build_obsidian_robot(optimized)):
            next_states.append(new_state)

        return next_states

    def just_mine(self) -> Self:

        new_state = copy.copy(self)
        new_state.mine()
        return new_state

    def build_ore_robot(self, check_bottleneck: bool = False) -> Self | None:
        if not self.can_afford(self.blueprint.ore_robot_cost):
            return

        if check_bottleneck and self.ore_robots >= self.blueprint.max_ore_cost:
            return

        new_state = copy.copy(self)
        new_state.deduce_cost(self.blueprint.ore_robot_cost)
        new_state.mine()
        new_state.ore_robots += 1
        return new_state

    def build_clay_robot(self, check_bottleneck: bool = False) -> Self | None:
        if not self.can_afford(self.blueprint.clay_robot_cost):
            return

        if check_bottleneck and self.clay_robots >= self.blueprint.max_clay_cost:
            return

        new_state = copy.copy(self)
        new_state.deduce_cost(self.blueprint.clay_robot_cost)
        new_state.mine()
        new_state.clay_robots += 1
        return new_state

    def build_obsidian_robot(self, check_bottleneck: bool = False) -> Self | None:
        if not self.can_afford(self.blueprint.obsidian_robot_cost):
            return

        if check_bottleneck and self.obsidian_robots >= self.blueprint.max_obsidian_cost:
            return

        new_state = copy.copy(self)
        new_state.deduce_cost(self.blueprint.obsidian_robot_cost)
        new_state.mine()
        new_state.obsidian_robots += 1
        return new_state

    def build_geode_robot(self) -> Self | None:
        if not self.can_afford(self.blueprint.geode_robot_cost):
            return

        new_state = copy.copy(self)
        new_state.deduce_cost(self.blueprint.geode_robot_cost)
        new_state.mine()
        new_state.geode_robots += 1
        return new_state


def job(blueprint: Blueprint, minutes: int):

    max_geodes = blueprint.max_geodes(minutes)
    quality = blueprint.blueprint_id * max_geodes
    print(f'Blueprint {blueprint.blueprint_id}: {max_geodes=}, {quality=}')
    return quality, max_geodes

def main(input_path: str, minutes: int):
    input_text = Path(input_path).read_text(encoding='utf-8')
    blueprints = [
        Blueprint.from_string_spec(spec)
        for spec in input_text.splitlines()
    ]

    with ProcessPoolExecutor(max_workers=10) as pool:
        results = [pool.submit(job, blueprint, minutes) for blueprint in blueprints]

        total_quality = 0
        for result in as_completed(results):
            total_quality += result.result()[0]

    print('Total quality:', total_quality)

def main_2(input_path: str, minutes: int):
    input_text = Path(input_path).read_text(encoding='utf-8')
    blueprints = [
        Blueprint.from_string_spec(spec)
        for spec in input_text.splitlines()
    ]

    blueprints = blueprints[:3]

    with ProcessPoolExecutor() as pool:
        results = [pool.submit(job, blueprint, minutes) for blueprint in blueprints]

        total_quality = 1
        for result in as_completed(results):
            total_quality *= result.result()[1]

    print('Total quality:', total_quality)


if __name__ == "__main__":
    MINUTES = 24
    MINUTES_2 = 32
    INPUT_PATH = './input.txt'
    # main(INPUT_PATH, MINUTES)
    main_2(INPUT_PATH, MINUTES_2)
