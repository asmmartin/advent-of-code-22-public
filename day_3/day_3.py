# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from typing import Iterable


class Rucksack:
    def __init__(self, items: str) -> None:
        item_count = len(items)
        self.compartments = [
            items[:item_count//2],
            items[item_count//2:]
        ]

    def get_repeated_item(self):
        items_sets = set(self.compartments[0]), set(self.compartments[1])
        repeated_items = items_sets[0].intersection(items_sets[1])
        try:
            return repeated_items.pop()
        except KeyError:
            return None

def get_item_priority(item: str):
    return ord(item) - 96 if item.islower() else ord(item) - 38

def find_badge(rucksack_group: Iterable[Rucksack]):
    items_sets = [
        set(rucksack.compartments[0] + rucksack.compartments[1])
        for rucksack in rucksack_group
    ]
    for item in items_sets[0]:
        if all(item in item_set for item_set in items_sets):
            return item
    return None


if __name__ == "__main__":

    INPUT_FILE_PATH = 'input.txt'
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        items_lists = [line for line in input_file.read().splitlines() if line]

    rucksacks = tuple(Rucksack(items) for items in items_lists)

    # PART 1
    priorities_sum = sum(
        get_item_priority(rucksack.get_repeated_item())
        for rucksack in rucksacks
    )
    print(f'The sum of priorities of repeated items is {priorities_sum}')

    # PART 2
    iters = [iter(rucksacks)] * 3
    groups = zip(*iters)

    badges = tuple(find_badge(group) for group in groups)
    badges_sum = sum(get_item_priority(badge) for badge in badges)
    print(f'The sum of priorities of badges is {badges_sum}')
