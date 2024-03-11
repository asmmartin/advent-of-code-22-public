# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import deque
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import logging

logger = logging.getLogger(__name__)

class Movement(Enum):
    SOUTH = (1, 0)
    EAST = (0, 1)
    STAY = (0, 0)
    NORTH = (-1, 0)
    WEST = (0, -1)

@dataclass(frozen=True)
class Blizzard:
    position: tuple[int, int]
    movement: Movement

@dataclass(unsafe_hash=True)
class Valley:
    def __init__(
        self,
        dimensions: tuple[int, int],
        blizzards:frozenset[Blizzard],
        start_point: tuple[int, int] | None = None,
        end_point: tuple[int, int] | None = None
    ) -> None:
        self.dimensions = dimensions
        self.blizzards = blizzards

        self.blizzard_positions = frozenset(
            blizzard.position for blizzard in blizzards
        )

        self.start_point = start_point or (0, 1)
        self.end_point = end_point or (dimensions[0] - 1, dimensions[1] - 2)

    @classmethod
    def from_string(cls, text: str) -> Self:
        text_lines = text.strip().splitlines()

        dimensions = (len(text_lines), len(text_lines[0]))

        blizzards = []
        for row, line in enumerate(text_lines):
            for col, character in enumerate(line):
                if character == '^':
                    movement = Movement.NORTH
                elif character == 'v':
                    movement = Movement.SOUTH
                elif character == '>':
                    movement = Movement.EAST
                elif character == '<':
                    movement = Movement.WEST
                else:
                    continue
                blizzards.append(Blizzard((row, col), movement))

        for col, character in enumerate(text_lines[0]):
            if character == '.':
                start_point = (0, col)
                break
        else:
            raise ValueError('No entry in the first row!')

        for col, character in enumerate(text_lines[-1]):
            if character == '.':
                end_point = (dimensions[0] - 1 , col)
                break
        else:
            raise ValueError('No exit in the last row!')

        return cls(
            blizzards=frozenset(blizzards),
            dimensions=dimensions,
            start_point=start_point,
            end_point=end_point
        )

    def is_clear(self, position: tuple[int, int]) -> bool:
        if position in self.blizzard_positions:
            return False
        if position in (self.start_point, self.end_point):
            return True
        if not 0 < position[0] < (self.dimensions[0] - 1):
            return False
        if not 0 < position[1] < (self.dimensions[1] - 1):
            return False
        return True

    def to_text(self, elf_position: tuple[int, int] | None = None) -> str:
        direction_symbols = {
            Movement.NORTH: '^',
            Movement.SOUTH: 'v',
            Movement.EAST: '>',
            Movement.WEST: '<'
        }

        tiles = [
            [[0, '.'] for _ in range(self.dimensions[1])]
            for _ in range(self.dimensions[0])
        ]

        for row in range(self.dimensions[0]):
            tiles[row][0] = [0, '#']
            tiles[row][-1] = [0, '#']
        for col in range(self.dimensions[1]):
            tiles[0][col] = [0, '#']
            tiles[-1][col] = [0, '#']

        tiles[self.start_point[0]][self.start_point[1]] = [0, '.']
        tiles[self.end_point[0]][self.end_point[1]] = [0, '.']

        if elf_position is not None:
            tiles[elf_position[0]][elf_position[1]] = [0, 'E']

        for blizzard in self.blizzards:
            tile = tiles[blizzard.position[0]][blizzard.position[1]]
            tile[0] += 1
            tile[1] = direction_symbols[blizzard.movement]

        text = '\n'.join(
            ''.join((tile[1] if tile[0] < 2 else str(tile[0])) for tile in row)
            for row in tiles
        )

        return text

class BlizzardsSimulator:
    def __init__(self, starting_valley: Valley) -> None:
        self.states = {0: starting_valley}
        self.loop_length: int | None = None

    def get_valley(self, minute: int):
        if self.loop_length is not None:
            minute = minute % self.loop_length
        if not minute in self.states:
            self.simulate_blizzards_until(minute)
        return self.states[minute]

    def move_blizzards(self, valley: Valley) -> Valley:
        new_blizzards = []

        for blizzard in valley.blizzards:
            new_position = (
                blizzard.position[0] + blizzard.movement.value[0],
                blizzard.position[1] + blizzard.movement.value[1],
            )
            new_position = (
                1 + (new_position[0] - 1) % (valley.dimensions[0] - 2),
                1 + (new_position[1] - 1) % (valley.dimensions[1] - 2),
            )
            new_blizzards.append(Blizzard(new_position, blizzard.movement))

        return Valley(
            dimensions=valley.dimensions,
            blizzards=frozenset(new_blizzards),
            start_point=valley.start_point,
            end_point=valley.end_point
        )

    def simulate_blizzards_until(self, minute: int) -> None:
        if minute in self.states:
            return
        last_minute = max(self.states.keys())
        while last_minute < minute:
            valley = self.states[last_minute]
            last_minute += 1
            self.states[last_minute] = self.move_blizzards(valley)

    def simulate_blizzards_until_loop(self) -> None:
        minute = 0
        valley = self.states[0]
        while True:
            valley = self.move_blizzards(valley)
            if valley.blizzards == self.states[0].blizzards:
                self.loop_length = minute + 1
                break
            minute += 1
            self.states[minute] = valley

    def equivalent_minute(self, minute: int) -> int:
        if self.loop_length is None:
            return minute
        return minute % self.loop_length

def find_path(
    valley: Valley,
    simulator: BlizzardsSimulator | None = None
):

    start = valley.start_point
    end = valley.end_point

    if not simulator:
        simulator = BlizzardsSimulator(valley)

    # BFS
    visited = set()
    to_visit = deque()
    to_visit.append((start,))
    while to_visit:
        path = to_visit.popleft()

        minute = len(path) - 1
        valley = simulator.get_valley(minute)

        if (simulator.equivalent_minute(minute), path[-1]) in visited:
            continue

        visited.add((simulator.equivalent_minute(minute), path[-1]))

        if path[-1] == end:
            return path

        next_valley = simulator.get_valley(minute + 1)

        position = path[-1]
        for movement in Movement:
            next_position = (
                position[0] + movement.value[0], position[1] + movement.value[1]
            )
            if not next_valley.is_clear(next_position):
                continue
            next_path = path + (next_position,)
            if (simulator.equivalent_minute(minute + 1), next_path[-1]) in visited:
                continue
            to_visit.append(next_path)


    raise ValueError('That valley has not a solution!!')

def main_1(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    valley = Valley.from_string(input_text)

    logger.debug('Pre-computing minutes...')
    simulator = BlizzardsSimulator(valley)
    simulator.simulate_blizzards_until_loop()
    logger.debug(f'Pre-computed minutes: {len(simulator.states)}')

    path = find_path(valley, simulator)
    solution = len(path) - 1
    print(f'Solution part 1: {solution} ({path=})')

def main_2(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')

    # Forward
    first_valley = Valley.from_string(input_text)
    first_simulator = BlizzardsSimulator(first_valley)
    first_path = find_path(first_valley, first_simulator)

    # Backward
    middle_valley = Valley(
        dimensions=first_valley.dimensions,
        start_point=first_valley.end_point,
        end_point=first_valley.start_point,
        blizzards=first_simulator.get_valley(len(first_path)-1).blizzards
    )
    middle_simulator = BlizzardsSimulator(middle_valley)
    middle_path = find_path(middle_valley, middle_simulator)

    # Forward again
    final_valley = Valley(
        dimensions=middle_valley.dimensions,
        start_point=middle_valley.end_point,
        end_point=middle_valley.start_point,
        blizzards=middle_simulator.get_valley(len(middle_path)-1).blizzards
    )
    final_simulator = BlizzardsSimulator(final_valley)
    final_path = find_path(final_valley, final_simulator)

    solution = len(first_path) + len(middle_path) + len(final_path) - 3
    print(f'Solution part 2: {solution}. Path: {first_path + middle_path + final_path}')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    INPUT_FILE = './input.txt'
    main_1(INPUT_FILE)
    main_2(INPUT_FILE)
