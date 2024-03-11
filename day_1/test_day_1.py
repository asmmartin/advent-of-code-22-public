# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

from pytest import fixture

from .day_1 import get_most_caloric_packs, input_to_ration_packs

@fixture
def input_text():
    return '1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000\n'

@fixture
def packs():
    return [
        [1000, 2000, 3000],
        [4000],
        [5000, 6000],
        [7000, 8000, 9000],
        [10000]
    ]

def test_input_to_ration_packs(input_text, packs):
    read_packs = input_to_ration_packs(input_text)
    assert read_packs == packs

def test_first_part(packs):

    most_caloric_pack = get_most_caloric_packs(packs)[0]
    assert sum(most_caloric_pack) == 24000

def test_second_part(packs):
    three_most_caloric_packs = get_most_caloric_packs(packs, 3)
    total_calories = sum(sum(pack) for pack in three_most_caloric_packs)
    assert total_calories == 45000
