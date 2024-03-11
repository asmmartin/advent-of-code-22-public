# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from collections import deque
import sys
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_text(cls, text: str) -> 'Point':
        text_x, text_y = text.split(',')
        return cls(x=int(text_x), y=int(text_y))

def path_from_text(text: str) -> set[Point]:
    pivot_point_texts = text.split(' -> ')
    points = [Point.from_text(pivot_point_texts.pop(0))]

    for pivot_text in pivot_point_texts:
        pivot = Point.from_text(pivot_text)
        current = points[-1]

        if current.x == pivot.x:
            min_y, max_y = min((current.y, pivot.y)), max((current.y, pivot.y))
            for point_y in range(min_y, max_y):
                points.append(Point(x=current.x, y=point_y))
        else:
            min_x, max_x = min((current.x, pivot.x)), max((current.x, pivot.x))
            for point_x in range(min_x, max_x):
                points.append(Point(x=point_x, y=current.y))

        points.append(pivot)

    return set(points)

class Wall:
    def __init__(
        self,
        rocks: set[Point],
        sand_source: Point = Point(500, 0),
        has_bottom: bool = False
    ) -> None:
        self.rocks = rocks
        self.sand_source = sand_source
        self.sands = set()
        self.has_bottom = has_bottom

        max_depth = max(point.y for point in rocks)
        self._max_depth = max_depth + 2 if has_bottom else max_depth

        self._previous_sand_path = deque((sand_source,))

    def place_sand(self) -> bool:
        while True:
            try:
                current = self._previous_sand_path[-1]
            except IndexError:
                return False

            # Check if it falling to the void
            if current.y >= self._max_depth:
                return False

            # Check if bottom has being reached
            if self.has_bottom and current.y + 1  == self._max_depth:
                self.sands.add(current)
                self._previous_sand_path.pop()
                return True

            below_left, below, below_right = (
                Point(current.x - 1, current.y + 1),
                Point(current.x    , current.y + 1),
                Point(current.x + 1, current.y + 1)
            )
            taken_points = self.sands.union(self.rocks)
            if below not in taken_points:
                current = below
            elif below_left not in taken_points:
                current = below_left
            elif below_right not in taken_points:
                current = below_right
            else:
                self.sands.add(current)
                self._previous_sand_path.pop()
                return True

            self._previous_sand_path.append(current)

    def fill_with_sand(self):
        while self.place_sand():
            pass

    def draw(self):
        relevant_points = {self.sand_source}.union(self.sands, self.rocks)
        min_x = min(point.x for point in relevant_points)
        min_y = min(point.y for point in relevant_points)
        max_x = max(point.x for point in relevant_points)
        max_y = max(point.y for point in self.rocks)

        if self.has_bottom:
            max_y += 2

        drawing = [
            ['.' for _ in range(max_x - min_x + 1)]
            for _ in range(max_y - min_y + 1)
        ]

        drawing[self.sand_source.y - min_y][self.sand_source.x - min_x] = '+'
        for sand in self.sands:
            drawing[sand.y - min_y][sand.x - min_x] = 'o'
        for rock in self.rocks:
            drawing[rock.y - min_y][rock.x - min_x] = '#'

        if self.has_bottom:
            for index, row in enumerate(drawing):
                drawing[index] = ['.', '.'] + row + ['.', '.']
            drawing[-1] = ['#' for _ in drawing[-1]]

        return '\n'.join([''.join(row) for row in drawing])

def main():
    path_texts = sys.stdin.read().splitlines()
    paths = [path_from_text(text) for text in path_texts]
    bottomless_wall = Wall(rocks=set().union(*paths))
    bottomless_wall.fill_with_sand()
    print(f'The bottomless full wall has {len(bottomless_wall.sands)} sand points')
    print()
    wall = Wall(rocks=set().union(*paths), has_bottom=True)
    while wall.place_sand():
        if not len(wall.sands) % 500:
            print(f'Current sands count: {len(wall.sands)}')
    print(f'The wall with bottom has {len(wall.sands)} sand points')


if __name__ == "__main__":
    main()
