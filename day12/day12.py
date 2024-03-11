# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import sys
from collections import deque


DIRECTIONS = {
    (1, 0): 'v',
    (0, 1): '>',
    (-1, 0): '^',
    (0, -1): '<'
}

def find_extremes(
    grid: list[str],
    start_letter: str | None = 'S',
    end_letter: str | None = 'E'
) -> tuple[tuple[int, int], tuple[int, int]]:
    start, end = None, None
    for i_row, row in enumerate(grid):
        for i_col, letter in enumerate(row):
            if not start and letter == start_letter:
                start = (i_row, i_col)
            elif not end and letter == end_letter:
                end = (i_row, i_col)
    return start, end

def calculate_height(letter: str) -> int:
    match letter:
        case 'S':
            return 0
        case 'E':
            return 25
        case _:
            return ord(letter) - 97

def get_valid_neighbours(
    grid: list[str],
    coords: tuple[int, int],
    reverse: bool = False
) -> list[tuple[int, int]]:

    valid_neighbours = []
    for deltas in DIRECTIONS:
        neighbour_x, neighbour_y = coords[0] + deltas[0], coords[1] + deltas[1]
        if not 0 <= neighbour_x < len(grid) or not 0 <= neighbour_y < len(grid[0]):
            continue

        current_value = calculate_height(grid[coords[0]][coords[1]])
        neighbour_value = calculate_height(grid[neighbour_x][neighbour_y])

        height_difference = neighbour_value - current_value
        if reverse:
            height_difference *= -1
        if height_difference <= 1:
            valid_neighbours.append((neighbour_x, neighbour_y))

    return valid_neighbours

def path_to_top(
    grid: list[str], hiking: bool = False
) -> list[tuple[int, int]]:

    if hiking:
        start, end = find_extremes(grid, 'E', None)
        target = 'a'
    else:
        start, end = find_extremes(grid)
        target = 'E'

    known_points = set()
    to_visit = deque()

    to_visit.append(((start), []))
    while to_visit:
        current_point, previous_points = to_visit.popleft()
        for neighbour in get_valid_neighbours(grid, current_point, hiking):
            if grid[neighbour[0]][neighbour[1]] == target:
                if hiking:
                    return (
                        start,
                        (previous_points + [current_point] + [neighbour])[:0:-1]
                    )
                else:
                    return (
                        (neighbour[0], neighbour[1]),
                        previous_points + [current_point]
                    )
            if neighbour in known_points:
                continue
            to_visit.append((neighbour, previous_points + [current_point]))
            known_points.add(neighbour)
    return end, None

def calculate_step(start: tuple[int, int], end: tuple[int, int]) -> str:
    deltas = end[0] - start[0], end[1] - start[1]
    return DIRECTIONS[deltas]

def draw_path(
    dimensions: tuple[int, int],
    steps: list[tuple[int, int]],
    end_tile: tuple[int, int]
):
    grid = [
        ['.' for _ in range(dimensions[1])]
        for _ in range(dimensions[0])
    ]

    grid[end_tile[0]][end_tile[1]] = 'E'
    path = steps + [end_tile]

    for index in range(len(steps)):
        current_tile, next_tile = path[index], path[index + 1]
        grid[current_tile[0]][current_tile[1]] = calculate_step(
            current_tile, next_tile
        )

    return '\n'.join([''.join(row) for row in grid])

def main():
    grid = [row.strip() for row in sys.stdin.readlines()]
    end_tile, path = path_to_top(grid)
    drawing = draw_path((len(grid), len(grid[0])), path, end_tile)
    print(drawing)
    print()
    print(f'{len(path)} steps to top!')
    print()

    print('Now the hiking path...')
    end_tile, path = path_to_top(grid, hiking=True)
    drawing = draw_path((len(grid), len(grid[0])), path, end_tile)
    print(drawing)
    print()
    print(f'{len(path)} steps to top!')

if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    main()
