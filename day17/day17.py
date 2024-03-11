# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

from collections import deque
from pathlib import Path
from typing import Generator

ROCKS = (
    {
        (0   ), (1   ), (2    ), (3    )
    },
    {
                (1+2j),
        (  1j), (1+1j), (2+1j),
                (1   )
    },
    {
                        (2+2j),
                        (2+1j),
        (0   ), (1   ), (2   )
    },
    {
        (  3j),
        (  2j),
        (  1j),
        (0   )
    },
    {
        (  1j), (1+1j),
        (0   ), (1   )
    }
)

DIRECTIONS = (1, -1, 1j, -1j)

def jets_generator(pattern: str) -> Generator[tuple[int, int], None, None]:

    if not pattern:
        raise ValueError('pattern not valid!')

    index = 0
    pattern_length = len(pattern)

    while True:
        yield (index, 1) if pattern[index] == '>' else (index, -1)
        index = (index + 1) % pattern_length

def rocks_generator() -> Generator[tuple[int, set[complex|int]], None, None]:
    index = 0
    while True:
        yield index, ROCKS[index] # type: ignore
        index = (index + 1) % 5

class Chamber:

    WIDTH = 7

    def __init__(
        self,
        pattern: str,
        starting_rocks: set[complex] | None = None
    ) -> None:
        self.jets_gen = jets_generator(pattern)
        self.rocks_gen = rocks_generator()
        self.rocks = starting_rocks if starting_rocks else set()
        self.rocks_height = -1
        self.current_rock = None

    def start_rock(self, rock: set[complex]) -> None:
        offset = 2 + (4 + self.rocks_height)*1j
        self.current_rock = {offset + coords for coords in rock}

    def move_rock(self, direction: complex) -> bool:
        if not self.current_rock:
            raise AttributeError('There is no rock falling!')

        new_tiles = {tile + direction for tile in self.current_rock}

        # Check collision with walls
        if any(not (0 <= tile.real < self.WIDTH) for tile in new_tiles):
            return False

        # Check collision with floor
        if any(not (0 <= tile.imag) for tile in new_tiles):
            return False

        # Check collision with other rocks
        if new_tiles.intersection(self.rocks):
            return False

        # Move correct
        self.current_rock = new_tiles
        return True

    def drop_rock(self) -> tuple[int, int]:

        rock_type_index, rock = next(self.rocks_gen)
        self.start_rock(rock)

        while True:

            jet_index, jet_movement = next(self.jets_gen)
            self.move_rock(jet_movement)
            if not self.move_rock(-1j):
                break

        self.rocks |= self.current_rock # type: ignore
        self.rocks_height = max(tile.imag for tile in self.rocks)

        return rock_type_index, jet_index

    def remove_non_relevant_rocks(self):

        relevant_rocks = set()

        # BFS to find all tiles exposed to surface
        visited = set()
        to_visit = deque()

        to_visit.append(2 + (1 + self.rocks_height)*1j)
        while to_visit:
            node_to_explore = to_visit.popleft()
            if node_to_explore not in visited:
                visited.add(node_to_explore)

                for direction in DIRECTIONS:
                    neighbour = node_to_explore + direction
                    if not 0 <= neighbour.real < self.WIDTH:
                        continue
                    if not 0 <= neighbour.imag <= 1 + self.rocks_height:
                        continue
                    if neighbour in self.rocks:
                        relevant_rocks.add(neighbour)
                    elif neighbour not in visited:
                        to_visit.append(neighbour)

        self.rocks = relevant_rocks

def normalize_rock_tiles(rock_tiles: set[complex]) -> set[complex]:
    base = min(tile.imag for tile in rock_tiles) * 1j
    return set(tile - base for tile in rock_tiles)

def main():
    jets_text = Path(INPUT_PATH).read_text(encoding='utf-8')
    chamber = Chamber(jets_text)

    for _ in range(2022):
        chamber.drop_rock()

    print(f'The height of the tower is {chamber.rocks_height + 1}')
    print(f'Rock count is {len(chamber.rocks)}')
    chamber.remove_non_relevant_rocks()
    print(f'Relevant rocks count is {len(chamber.rocks)}')

    # Part 2

    jets_text = Path(INPUT_PATH).read_text(encoding='utf-8')
    chamber = Chamber(jets_text)
    history = {}

    iterations = 1_000_000_000_000

    # Avoid linter complaining...
    rock_index = 0
    history_key = None

    for rock_index in range(iterations):
        rock_type_index, jet_index = chamber.drop_rock()
        chamber.remove_non_relevant_rocks()
        normalized_rocks = frozenset(normalize_rock_tiles(chamber.rocks))
        history_key = rock_type_index, jet_index, normalized_rocks

        if history_key in history:
            break

        history[history_key] = rock_index, chamber.rocks_height

    base_loop_index = history[history_key][0]
    base_loop_height = history[history_key][1]
    loop_length = rock_index - base_loop_index
    loop_height_delta = chamber.rocks_height - base_loop_height

    number_of_remaining_loops = (iterations - rock_index - 1) // loop_length
    remaining_rocks = (iterations - rock_index - 1) % loop_length

    for _ in range(remaining_rocks):
        chamber.drop_rock()

    tower_height = chamber.rocks_height + loop_height_delta * number_of_remaining_loops + 1

    print(f'Second part: {tower_height=}')


if __name__ == "__main__":
    INPUT_PATH = './input.txt'
    main()
