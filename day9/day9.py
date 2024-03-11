# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    UP_RIGHT = (1, 1)
    UP_LEFT = (-1, 1)
    DOWN_RIGHT = (1, -1)
    DOWN_LEFT = (-1, -1)

    STAY = (0, 0)

    @classmethod
    def from_letter(cls, letter: str):
        match letter:
            case 'U': return cls.UP
            case 'D': return cls.DOWN
            case 'L': return cls.LEFT
            case 'R': return cls.RIGHT
            case unknown: raise ValueError(f'{unknown} is not a valid direction!')

def parse_moves(moves_text: str):
    moves = []
    lines = moves_text.splitlines()
    for line in lines:
        direction, count = line.split()
        moves.extend(Direction.from_letter(direction) for _ in range(int(count)))
    return moves

@dataclass
class Knot:
    # pylint: disable=invalid-name
    x: int = 0
    y: int = 0

    def squared_distance_to(self, other_knot: 'Knot'):
        return (self.x - other_knot.x)**2 + (self.y - other_knot.y)**2

class Rope:
    def __init__(self, knots: tuple[Knot] = None) -> None:
        self.knots = knots or (Knot(), Knot())
        self.knots = tuple(self.knots)

        self.visited_by_tail = set()
        tail = self.knots[-1]
        self.visited_by_tail.add((tail.x, tail.y))

        for knot_index in range(len(self.knots) - 1):
            current_knot = self.knots[knot_index]
            next_knot = self.knots[knot_index + 1]
            distance_square = current_knot.squared_distance_to(next_knot)
            if distance_square > 2:
                raise ValueError(
                    f'Knots {knot_index} and {knot_index+1} are not touching each other'
                )

    def move_knot(self, direction: Direction, knot_index: int = 0) -> None:
        x_inc, y_inc = direction.value
        knot = self.knots[knot_index]

        knot.x += x_inc
        knot.y += y_inc

        if id(knot) == id(self.knots[-1]):
            self.visited_by_tail.add((knot.x, knot.y))
            return

        next_knot = self.knots[knot_index + 1]
        relative_position = (knot.x - next_knot.x, knot.y - next_knot.y)

        match relative_position:
            case (2, 0):
                next_knot_move = Direction.RIGHT
            case (-2, 0):
                next_knot_move = Direction.LEFT
            case (0, 2):
                next_knot_move = Direction.UP
            case (0, -2):
                next_knot_move = Direction.DOWN
            case (2, 1) | (1, 2) | (2, 2):
                next_knot_move = Direction.UP_RIGHT
            case (-2, 1) | (-1, 2) | (-2, 2):
                next_knot_move = Direction.UP_LEFT
            case (2, -1) | (1, -2) | (2, -2):
                next_knot_move = Direction.DOWN_RIGHT
            case (-2, -1) | (-1, -2) | (-2, -2):
                next_knot_move = Direction.DOWN_LEFT
            case _:
                next_knot_move = Direction.STAY
        self.move_knot(next_knot_move, knot_index=knot_index+1)

def main():
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        input_text = input_file.read()

    rope = Rope()
    moves = parse_moves(input_text)
    for move in moves:
        rope.move_knot(move)
    print(f'The tail of the short rope visited {len(rope.visited_by_tail)} different tiles')

    rope = Rope(tuple(Knot() for _ in range(10)))
    for move in moves:
        rope.move_knot(move)
    print(f'The tail of the long rope visited {len(rope.visited_by_tail)} different tiles')


if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    main()
