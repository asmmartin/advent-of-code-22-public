# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest

from .day5 import (
    text_to_crate_stacks, Instruction, CrateMover9000, CrateMover9001)

@pytest.fixture
def example_crate_stacks():
    return [
        list(('[Z]', '[N]')),
        list(('[M]', '[C]', '[D]')),
        list(('[P]',))
    ]

@pytest.fixture
def example_instructions():
    return [
        Instruction(amount=1, origin=2, destination=1),
        Instruction(amount=3, origin=1, destination=3),
        Instruction(amount=2, origin=2, destination=1),
        Instruction(amount=1, origin=1, destination=2),
    ]

def test_text_to_crate_stacks(example_crate_stacks):
    example_text = (
        '    [D]\n'
        '[N] [C]\n'
        '[Z] [M] [P]\n'
        ' 1   2   3 '
    )

    stacks = text_to_crate_stacks(example_text)
    assert len(stacks) == 3
    assert stacks == example_crate_stacks

def test_parse_instruction():

    example_texts = (
        'move 1 from 2 to 1',
        'move 3 from 1 to 3',
        'move 2 from 2 to 1',
        'move 1 from 1 to 2',
    )

    instructions = [Instruction.from_string(sample) for sample in example_texts]

    assert tuple((i.amount, i.origin, i.destination) for i in instructions) == (
        (1, 2, 1),
        (3, 1, 3),
        (2, 2, 1),
        (1, 1, 2),
    )

def test_cratemover9000(example_crate_stacks, example_instructions):

    crane = CrateMover9000()

    for instruction in example_instructions:
        crane.execute(instruction, example_crate_stacks)

    assert example_crate_stacks == [
        list(('[C]',)),
        list(('[M]',)),
        list(('[P]', '[D]', '[N]', '[Z]'))
    ]

def test_cratemover9001(example_crate_stacks, example_instructions):

    crane = CrateMover9001()

    for instruction in example_instructions:
        crane.execute(instruction, example_crate_stacks)

    assert example_crate_stacks == [
        list(('[M]',)),
        list(('[C]',)),
        list(('[P]', '[Z]', '[N]', '[D]'))
    ]
