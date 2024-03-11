# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import Counter
from pathlib import Path
from typing import Self

Elf = tuple[int, int]
Movement = tuple[int, int]

class Groove:

    def __init__(self, elves: set[Elf]):
        self.elves = elves
        self.check_functions = [
            self.check_north_is_empty,
            self.check_south_is_empty,
            self.check_west_is_empty,
            self.check_east_is_empty
        ]

    @classmethod
    def from_text(cls, text_map: str) -> Self:

        elf_symbol = '#'

        elves = set()
        lines = text_map.strip().splitlines()
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == elf_symbol:
                    elves.add((i, j))
        return cls(elves=elves)

    def check_north_is_empty(self, elf: Elf) -> Movement:
        if (
            (elf[0] - 1, elf[1] - 1) in self.elves or
            (elf[0] - 1, elf[1]    ) in self.elves or
            (elf[0] - 1, elf[1] + 1) in self.elves
        ):
            return (0, 0)
        return (-1, 0)

    def check_south_is_empty(self, elf: Elf) -> Movement:
        if (
            (elf[0] + 1, elf[1] - 1) in self.elves or
            (elf[0] + 1, elf[1]    ) in self.elves or
            (elf[0] + 1, elf[1] + 1) in self.elves
        ):
            return (0, 0)
        return (1, 0)

    def check_east_is_empty(self, elf: Elf) -> Movement:
        if (
            (elf[0] - 1, elf[1] + 1) in self.elves or
            (elf[0]    , elf[1] + 1) in self.elves or
            (elf[0] + 1, elf[1] + 1) in self.elves
        ):
            return (0, 0)
        return (0, 1)

    def check_west_is_empty(self, elf: Elf) -> Movement:
        if (
            (elf[0] - 1, elf[1] - 1) in self.elves or
            (elf[0]    , elf[1] - 1) in self.elves or
            (elf[0] + 1, elf[1] - 1) in self.elves
        ):
            return (0, 0)
        return (0, -1)

    def check_loneliness(self, elf: Elf) -> bool:
        for check_function in self.check_functions:
            if check_function(elf) == (0, 0):
                return False
        return True

    def rotate_check_functions(self):
        self.check_functions = self.check_functions[1:] + [self.check_functions[0]]

    def propose_elves(self) -> dict[Elf, Elf]:
        proposed = {}
        for elf in self.elves:
            if self.check_loneliness(elf):
                proposed[elf] = elf
                continue
            for check_function in self.check_functions:
                movement = check_function(elf)
                if movement != (0, 0):
                    proposed[elf] = (elf[0] + movement[0], elf[1] + movement[1])
                    break
            else:
                proposed[elf] = elf
        return proposed

    def round(self) -> bool:

        new_elves = set()
        proposed = self.propose_elves()
        proposed_new_elves = Counter(proposed.values())

        for old_elf, new_elf in proposed.items():
            if proposed_new_elves[new_elf] > 1:
                new_elves.add(old_elf)
            else:
                new_elves.add(new_elf)

        if self.elves == new_elves:
            return False

        self.elves = new_elves
        self.rotate_check_functions()
        return True

    def go_until_still(self) -> int:
        rounds_count = 0
        while True:
            rounds_count += 1
            if not self.round():
                return rounds_count

    @property
    def soil(self) -> int:
        min_row = min(elf[0] for elf in self.elves)
        max_row = max(elf[0] for elf in self.elves)
        min_col = min(elf[1] for elf in self.elves)
        max_col = max(elf[1] for elf in self.elves)

        tiles = (max_row - min_row + 1) * (max_col - min_col + 1)
        return tiles - len(self.elves)

def main_1(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    groove = Groove.from_text(input_text)
    for _ in range(10):
        groove.round()
    solution = groove.soil
    print(f'Solution part 1: {solution}')

def main_2(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    groove = Groove.from_text(input_text)
    solution = groove.go_until_still()
    print(f'Solution part 2: {solution}')

if __name__ == "__main__":
    INPUT_FILE = './input.txt'
    main_1(INPUT_FILE)
    main_2(INPUT_FILE)
