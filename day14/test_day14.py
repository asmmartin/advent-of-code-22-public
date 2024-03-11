# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest
import day14

SAMPLE_ROCK_PATHS = (
    '498,4 -> 498,6 -> 496,6\n'
    '503,4 -> 502,4 -> 502,9 -> 494,9'
)

@pytest.fixture
def sample_wall():
    rocks = {
        day14.Point(498,4), day14.Point(498,5), day14.Point(498,6),
        day14.Point(497,6), day14.Point(496,6), day14.Point(503,4),
        day14.Point(502,4), day14.Point(502,5), day14.Point(502,6),
        day14.Point(502,7), day14.Point(502,8), day14.Point(502,9),
        day14.Point(501,9), day14.Point(500,9), day14.Point(499,9),
        day14.Point(498,9), day14.Point(497,9), day14.Point(496,9),
        day14.Point(495,9), day14.Point(494,9)
    }
    return day14.Wall(rocks=rocks)

@pytest.fixture
def sample_wall_with_bottom():
    rocks = {
        day14.Point(498,4), day14.Point(498,5), day14.Point(498,6),
        day14.Point(497,6), day14.Point(496,6), day14.Point(503,4),
        day14.Point(502,4), day14.Point(502,5), day14.Point(502,6),
        day14.Point(502,7), day14.Point(502,8), day14.Point(502,9),
        day14.Point(501,9), day14.Point(500,9), day14.Point(499,9),
        day14.Point(498,9), day14.Point(497,9), day14.Point(496,9),
        day14.Point(495,9), day14.Point(494,9)
    }
    return day14.Wall(rocks=rocks, has_bottom=True)


def test_points_from_text():
    assert day14.Point.from_text('498,4') == day14.Point(498, 4)
    assert day14.Point.from_text('502,9') == day14.Point(502, 9)

def test_paths_from_text():
    text_paths = [path.strip() for path in SAMPLE_ROCK_PATHS.splitlines()]
    paths = [day14.path_from_text(text_path) for text_path in text_paths]

    assert paths[0] == {
        (498,4), (498,5), (498,6), (497,6), (496,6)
    }
    assert paths[1] == {
        (503,4), (502,4), (502,5), (502,6), (502,7), (502,8), (502,9), (501,9),
        (500,9), (499,9), (498,9), (497,9), (496,9), (495,9), (494,9)
    }

def test_wall():
    rocks = {
        day14.Point(498,4), day14.Point(498,5), day14.Point(498,6),
        day14.Point(497,6), day14.Point(496,6), day14.Point(503,4),
        day14.Point(502,4), day14.Point(502,5), day14.Point(502,6),
        day14.Point(502,7), day14.Point(502,8), day14.Point(502,9),
        day14.Point(501,9), day14.Point(500,9), day14.Point(499,9),
        day14.Point(498,9), day14.Point(497,9), day14.Point(496,9),
        day14.Point(495,9), day14.Point(494,9)
    }
    wall = day14.Wall(rocks=rocks, sand_source=day14.Point(500, 0))
    assert wall
    assert wall._max_depth == 9 # pylint: disable=protected-access

def test_wall_place_sand(sample_wall):
    for _ in range(5):
        sample_wall.place_sand()
    assert sample_wall.sands == {
        day14.Point(500,8), day14.Point(499,8), day14.Point(501,8),
        day14.Point(500,7), day14.Point(498,8)
    }

def test_wall_place_sand_all_sample(sample_wall):
    for _ in range(24):
        sample_wall.place_sand()
    assert sample_wall.place_sand() is False
    assert len(sample_wall.sands) == 24

def test_wall_fill_with_sand(sample_wall):
    sample_wall.fill_with_sand()
    assert len(sample_wall.sands) == 24

def test_wall_with_bottom_fill_with_sand(sample_wall_with_bottom):
    sample_wall_with_bottom.fill_with_sand()
    assert len(sample_wall_with_bottom.sands) == 93

def test_wall_draw(sample_wall, sample_wall_with_bottom):
    sample_wall.fill_with_sand()
    drawing = sample_wall.draw()
    assert drawing == (
        "......+...\n"
        "..........\n"
        "......o...\n"
        ".....ooo..\n"
        "....#ooo##\n"
        "...o#ooo#.\n"
        "..###ooo#.\n"
        "....oooo#.\n"
        ".o.ooooo#.\n"
        "#########."
    )

    sample_wall_with_bottom.fill_with_sand()
    drawing = sample_wall_with_bottom.draw()
    assert drawing == (
        '............o............\n'
        '...........ooo...........\n'
        '..........ooooo..........\n'
        '.........ooooooo.........\n'
        '........oo#ooo##o........\n'
        '.......ooo#ooo#ooo.......\n'
        '......oo###ooo#oooo......\n'
        '.....oooo.oooo#ooooo.....\n'
        '....oooooooooo#oooooo....\n'
        '...ooo#########ooooooo...\n'
        '..ooooo.......ooooooooo..\n'
        '#########################'
    )
