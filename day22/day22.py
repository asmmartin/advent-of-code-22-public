# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from pathlib import Path
import re
from collections import namedtuple

Direction = namedtuple('direction', ['dy', 'dx', 'symbol'])

DIRECTIONS = [
    Direction(dy=0, dx=1, symbol='>'),
    Direction(dy=1, dx=0, symbol='v'),
    Direction(dy=0, dx=-1, symbol='<'),
    Direction(dy=-1, dx=0, symbol='^')
]


def parse_instructions(instructions_text: str) -> list[int|str]:
    to_parse = instructions_text
    advance_pattern = re.compile(r'(\d+)(.*)')
    turn_pattern = re.compile(r'([L|R])(.*)')

    instructions = []

    while to_parse:
        try:
            if (match := advance_pattern.match(to_parse)):
                instructions.append(int(match.group(1)))
                to_parse = match.group(2)
            elif (match := turn_pattern.match(to_parse)):
                instructions.append(match.group(1))
                to_parse = match.group(2)
            else:
                raise ValueError('Invalid text')
        except IndexError:
            break

    return instructions

class Board:

    VOID = ' '
    WALL = '#'

    def __init__(
        self,
        layout: str,
        edges: dict[tuple[int, int, int], tuple[int, int, int]] | None = None
    ) -> None:
        layout_lines = [line for line in layout.splitlines() if line]
        self.layout = [
            list(line) for line in layout_lines
        ]
        self.edges = edges or {}

        self.width = max(len(row) for row in self.layout)
        self.height = len(self.layout)
        self.current_direction_index = 0

        for row in self.layout:
            while len(row) < self.width:
                row.append(self.VOID)

        for i, tile in enumerate(self.layout[0]):
            if tile not in (self.VOID, self.WALL):
                self.current_tile_coords = (0, i)
                break
        else:
            raise ValueError('First row does not have a valid starting tile!')

    @property
    def next_tile_coords(self) -> tuple[int, int]:

        edge_next_tile = self.edges.get(
            (*self.current_tile_coords, self.current_direction_index) # type: ignore
        )
        if edge_next_tile:
            return edge_next_tile[0:2]

        cursor = self.current_tile_coords
        direction = DIRECTIONS[self.current_direction_index]
        while True:
            cursor = (
                (cursor[0] + direction.dy) % self.height,
                (cursor[1] + direction.dx) % self.width,
            )
            if self.layout[cursor[0]][cursor[1]] != self.VOID:
                return cursor

    @property
    def next_direction_index(self) -> int:

        edge_next_tile = self.edges.get(
            (*self.current_tile_coords, self.current_direction_index) # type: ignore
        )
        if edge_next_tile:
            return edge_next_tile[2]
        return self.current_direction_index

    @property
    def next_tile(self) -> str:
        return self.layout[self.next_tile_coords[0]][self.next_tile_coords[1]]

    @property
    def password(self) -> int:
        return (
            (self.current_tile_coords[0] + 1) * 1000 +
            (self.current_tile_coords[1] + 1) * 4 +
            self.current_direction_index
        )

    def apply_instruction(self, instruction: str | int):
        match instruction:
            case 'R':
                self.current_direction_index = (self.current_direction_index + 1) % 4
            case 'L':
                self.current_direction_index = (self.current_direction_index - 1) % 4
            case number if isinstance(number, int):
                self.advance(steps=number)
            case _:
                raise ValueError(f'{instruction} is not a valid instruction!')

    def advance(self, steps: int):
        for _ in range(steps):
            if self.next_tile == self.WALL:
                break
            (self.current_tile_coords, self.current_direction_index) = (
                self.next_tile_coords, self.next_direction_index
            )

def main_1(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    input_text_lines = input_text.splitlines()
    instructions_text = input_text_lines[-1]
    layout_text = '\n'.join(input_text_lines[:-2])

    instructions = parse_instructions(instructions_text)
    board = Board(layout=layout_text)
    for instruction in instructions:
        board.apply_instruction(instruction)

    print(f'Solution part 1: {board.password}')

def main_2(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    input_text_lines = input_text.splitlines()
    instructions_text = input_text_lines[-1]
    layout_text = '\n'.join(input_text_lines[:-2])

    instructions = parse_instructions(instructions_text)

    edges = {}

    edges.update({(0, 100+i, 3): (199, i, 3) for i in range(50)})
    edges.update({(0, 50+i, 3): (150+i, 0, 0) for i in range(50)})
    edges.update({(i, 50, 2): (149-i, 0, 0) for i in range(50)})
    edges.update({(50+i, 50, 2): (100, i, 1) for i in range(50)})
    edges.update({(49, 100+i, 1): (50+i, 99, 2) for i in range(50)})
    edges.update({(i, 149, 0): (149-i, 99, 2) for i in range(50)})
    edges.update({(149, 50+i, 1): (150+i, 49, 2) for i in range(50)})

    reverse_edges = {}
    for k, v in edges.items():
        reverse_edges[(v[0], v[1], (v[2] + 2) % 4)] = (k[0], k[1], (k[2] + 2) % 4)
    edges.update(reverse_edges)

    board = Board(layout=layout_text, edges=edges)
    for instruction in instructions:
        board.apply_instruction(instruction)

    print(f'Solution part 2: {board.password}')

if __name__ == "__main__":
    INPUT_FILE = './input.txt'
    main_1(INPUT_FILE)
    main_2(INPUT_FILE)
