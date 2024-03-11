# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest

from day6 import get_start_of_message_index

@pytest.fixture
def buffer_examples_1():
    return [
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    ]

@pytest.fixture
def buffer_examples_2():
    return [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    ]

def test_example_part_1(buffer_examples_1):
    expected_results = 5, 6, 10, 11

    for buffer, result in zip(buffer_examples_1, expected_results):
        assert get_start_of_message_index(buffer) == result

def test_example_part_2(buffer_examples_2):
    expected_results = 19, 23, 23, 29, 26

    for buffer, result in zip(buffer_examples_2, expected_results):
        assert get_start_of_message_index(buffer, marker_length=14) == result
