# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from math import prod


class TreeGrid:
    def __init__(self, trees: list[list[int]]) -> None:
        self.trees = trees
        self._rows = trees
        self._columns = [list(col) for col in zip(*trees)]

        self.max_row_index = len(self._rows) - 1
        self.max_col_index = len(self._columns) - 1

    @classmethod
    def from_text(cls, text: str) -> 'TreeGrid':
        trees = list(
            list(int(tree) for tree in row)
            for row in text.splitlines()
        )
        return cls(trees)

    def get_trees_visibility(self) -> list[list[bool]]:
        visibility = [[True for _ in row] for row in self.trees]
        for row_index, row in enumerate(self.trees):
            for col_index, _ in enumerate(row):
                visibility[row_index][col_index] = self.is_tree_visible(
                    row_index, col_index
                )
        return visibility

    def is_tree_visible(self, row_index: int, col_index: int) -> bool:
        if (
            row_index in (0, self.max_row_index) or
            col_index in (0, self.max_col_index)
        ):
            return True

        tallest_from_west = max(self._rows[row_index][:col_index])
        tallest_from_east = max(self._rows[row_index][col_index + 1 :])
        tallest_from_north = max(self._columns[col_index][:row_index])
        tallest_from_south = max(self._columns[col_index][row_index + 1 :])

        return any(
            self.trees[row_index][col_index] > tree
            for tree in (
                tallest_from_west,
                tallest_from_east,
                tallest_from_north,
                tallest_from_south,
            )
        )

    def get_tree_scenic_score(self, row_index: int, col_index: int) -> int:
        tree_lines = {
            'west' : self._rows[row_index][:col_index][::-1],
            'east' : self._rows[row_index][col_index + 1 :],
            'north' : self._columns[col_index][:row_index][::-1],
            'south' : self._columns[col_index][row_index + 1 :]
        }

        tree = self.trees[row_index][col_index]
        scores = [
            self.calculate_tree_viewing_distance(tree, tree_line)
            for tree_line in tree_lines.values()
        ]
        return prod(scores)


    def calculate_tree_viewing_distance(
        self, tree_height: int, tree_line: list[int]
    ) -> int:
        viewing_distance = 0
        for tree in tree_line:
            viewing_distance += 1
            if tree >= tree_height:
                break
        return viewing_distance

    def get_trees_scenic_scores(self) -> list[list[int]]:
        scores = [[0 for _ in row] for row in self.trees]
        for row_index, row in enumerate(self.trees):
            for col_index, _ in enumerate(row):
                scores[row_index][col_index] = self.get_tree_scenic_score(
                    row_index, col_index
                )
        return scores

def main():
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        input_text = input_file.read()

    grid = TreeGrid.from_text(input_text)
    visibility = grid.get_trees_visibility()
    visible_count = sum(sum(tree for tree in row) for row in visibility)
    print(f'There are {visible_count} visible trees from outside the grid.')

    scenic_scores = grid.get_trees_scenic_scores()
    max_score = max(max(score for score in row) for row in scenic_scores)
    print(f'The max scenic score is {max_score}')



if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    SMALL_DIRECTORY_THRESHOLD = 100_000
    TOTAL_SPACE = 70_000_000
    UPDATE_SPACE_REQUIRED = 30_000_000
    main()
