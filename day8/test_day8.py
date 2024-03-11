# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest

from day8 import TreeGrid

@pytest.fixture
def example_grid_text():
    return (
        "30373\n"
        "25512\n"
        "65332\n"
        "33549\n"
        "35390\n"
    )

@pytest.fixture
def example_tree_grid():
    return TreeGrid([
        [3,0,3,7,3],
        [2,5,5,1,2],
        [6,5,3,3,2],
        [3,3,5,4,9],
        [3,5,3,9,0]
    ])

def test_grid_from_text(example_grid_text):
    grid = TreeGrid.from_text(example_grid_text)
    assert grid.trees == [
        [3,0,3,7,3],
        [2,5,5,1,2],
        [6,5,3,3,2],
        [3,3,5,4,9],
        [3,5,3,9,0]
    ]

def test_get_trees_visibility(example_tree_grid):

    visibility = example_tree_grid.get_trees_visibility()

    assert visibility == [
        [True, True, True, True, True,],
        [True, True, True, False, True,],
        [True, True, False, True, True,],
        [True, False, True, False, True,],
        [True, True, True, True, True,],
    ]

    assert sum(sum(tree for tree in row) for row in visibility) == 21

def test_get_tree_scenic_score(example_tree_grid):
    assert example_tree_grid.get_tree_scenic_score(1, 2) == 4
    assert example_tree_grid.get_tree_scenic_score(3, 2) == 8

def test_get_trees_scenic_scores(example_tree_grid):
    scenic_scores = example_tree_grid.get_trees_scenic_scores()
    assert max(max(score for score in row) for row in scenic_scores) == 8
