'''Day 1 solution

https://adventofcode.com/2022/day/1
'''

# pylint: disable=missing-function-docstring

from typing import List

def input_to_ration_packs(text: str) -> List[List[int]]:

    packs = text.split('\n\n')
    packs = [pack.split('\n') for pack in packs]
    packs = [
        [int(ration) for ration in pack if ration]
        for pack in packs
    ]
    return packs

def get_most_caloric_packs(packs: List[List[int]], amount: int = 1) -> List[List[int]]:
    return sorted(packs, key=sum, reverse=True)[:amount]

def main(rations_text: str) -> None:

    packs = input_to_ration_packs(rations_text)

    # PART 1
    most_caloric_pack = get_most_caloric_packs(packs)[0]
    print(f'The most caloric pack has {sum(most_caloric_pack)} calories')

    # PART 2
    three_most_caloric_packs = get_most_caloric_packs(packs, 3)
    total_calories = sum(sum(pack) for pack in three_most_caloric_packs)
    print(f'The 3 most caloric packs add up to {total_calories} calories')

if __name__ == '__main__':

    INPUT_FILE = 'input.txt'

    with open(INPUT_FILE, encoding='utf-8') as f:
        input_text = f.read()

    main(input_text)
