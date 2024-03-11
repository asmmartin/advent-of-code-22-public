# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-name-in-module
# pylint: disable=redefined-outer-name

import pytest
from .day_3 import Rucksack, get_item_priority, find_badge

@pytest.fixture
def example_inputs():
    return [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw"
    ]

def test_rucksack(example_inputs):

    rucksack = Rucksack(example_inputs[0])
    assert rucksack
    assert len(rucksack.compartments[0]) == len(rucksack.compartments[1])

def test_find_repeated_item(example_inputs):
    rucksacks = [Rucksack(items) for items in example_inputs]
    repeated_items = ('p', 'L', 'P', 'v', 't', 's')

    for index, rucksack in enumerate(rucksacks):
        assert rucksack.get_repeated_item() == repeated_items[index]

def test_get_item_priority():
    repeated_items = ['p', 'L', 'P', 'v', 't', 's']
    priorities = tuple(get_item_priority(item) for item in repeated_items)
    assert priorities == (16, 38, 42, 22, 20, 19)

def test_find_badge(example_inputs):
    rucksacks = [Rucksack(items) for items in example_inputs]
    iters = [iter(rucksacks)] * 3
    groups = zip(*iters)

    badges = tuple(find_badge(group) for group in groups)

    assert badges == ('r', 'Z')
