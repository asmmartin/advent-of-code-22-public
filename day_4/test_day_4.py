# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest
from .day_4 import SectionRange

@pytest.fixture
def example_ranges():
    text = (
        ('2-4', '6-8'),
        ('2-3', '4-5'),
        ('5-7', '7-9'),
        ('2-8', '3-7'),
        ('6-6', '4-6'),
        ('2-6', '4-8'),
    )

    return [
        (SectionRange.from_string(first), SectionRange.from_string(second))
        for (first, second) in text
    ]


def test_section_range_from_string():
    section_range_one = SectionRange.from_string('2-9')
    section_range_two = SectionRange.from_string('5-5')

    assert section_range_one.sections == {2, 3, 4, 5, 6, 7, 8, 9}
    assert section_range_two.sections == {5}

def test_contains(example_ranges):

    assert example_ranges[3][0].contains(example_ranges[3][1])
    assert example_ranges[4][1].contains(example_ranges[4][0])
    assert not example_ranges[1][0].contains(example_ranges[1][1])

def test_calculate_intersection(example_ranges):

    intersections = {
        2: {7},
        3: {3, 4, 5, 6, 7},
        4: {6},
        5: {4, 5, 6}
    }

    for index, intersection in intersections.items():
        first, second = example_ranges[index][0], example_ranges[index][1]
        assert first.calculate_intersection(second) == intersection


def test_overlaps(example_ranges):

    assert not example_ranges[0][0].overlaps(example_ranges[0][1])
    assert not example_ranges[1][0].overlaps(example_ranges[1][1])
    assert example_ranges[2][0].overlaps(example_ranges[2][1])
    assert example_ranges[3][0].overlaps(example_ranges[3][1])
    assert example_ranges[4][0].overlaps(example_ranges[4][1])
    assert example_ranges[5][0].overlaps(example_ranges[5][1])
