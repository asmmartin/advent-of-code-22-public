# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest

from day25 import (
    snafu_to_decimal, decimal_to_snafu,
    snafu_to_snafu_ints, snafu_ints_to_snafu
)

@pytest.fixture(name='decimal_to_snafu_examples')
def decimal_to_snafu_examples_fixture():
    return {
        "1": "1",
        "2": "2",
        "3": "1=",
        "4": "1-",
        "5": "10",
        "6": "11",
        "7": "12",
        "8": "2=",
        "9": "2-",
        "10": "20",
        "15": "1=0",
        "20": "1-0",
        "2022": "1=11-2",
        "12345": "1-0---0",
        "314159265": "1121-1110-1=0",
    }

@pytest.fixture(name='snafu_to_decimal_examples')
def snafu_to_decimal_examples_fixture():
    return {
        "1=-0-2": "1747",
        "12111": "906",
        "2=0=": "198",
        "21": "11",
        "2=01": "201",
        "111": "31",
        "20012": "1257",
        "112": "32",
        "1=-1=": "353",
        "1-12": "107",
        "12": "7",
        "1=": "3",
        "122": "37",
    }

def test_snafu_to_snafu_ints(snafu_to_decimal_examples):

    snafu_ints = {
        snafu: snafu_to_snafu_ints(snafu)
        for snafu in snafu_to_decimal_examples.keys()
    }

    assert snafu_ints == {
        "1=-0-2": (1, -2, -1, 0, -1, 2),
        "12111": (1, 2, 1, 1, 1),
        "2=0=": (2, -2, 0, -2),
        "21": (2, 1),
        "2=01": (2, -2, 0, 1),
        "111": (1, 1, 1),
        "20012": (2, 0, 0, 1, 2),
        "112": (1, 1, 2),
        "1=-1=": (1, -2, -1, 1, -2),
        "1-12": (1, -1, 1, 2),
        "12": (1, 2),
        "1=": (1, -2),
        "122": (1, 2, 2),
    }

def test_snafu_ints_to_snafu():

    snafu_ints_examples = (
        (1, -2, -1, 0, -1, 2),
        (1, 2, 1, 1, 1),
        (2, -2, 0, -2),
        (2, 1),
        (2, -2, 0, 1),
        (1, 1, 1),
        (2, 0, 0, 1, 2),
        (1, 1, 2),
        (1, -2, -1, 1, -2),
        (1, -1, 1, 2),
        (1, 2),
        (1, -2),
        (1, 2, 2),
    )

    snafus = {
        snafu_ints: snafu_ints_to_snafu(snafu_ints)
        for snafu_ints in snafu_ints_examples
    }

    assert snafus == {
        (1, -2, -1, 0, -1, 2): "1=-0-2",
        (1, 2, 1, 1, 1): "12111",
        (2, -2, 0, -2): "2=0=",
        (2, 1): "21",
        (2, -2, 0, 1): "2=01",
        (1, 1, 1): "111",
        (2, 0, 0, 1, 2): "20012",
        (1, 1, 2): "112",
        (1, -2, -1, 1, -2): "1=-1=",
        (1, -1, 1, 2): "1-12",
        (1, 2): "12",
        (1, -2): "1=",
        (1, 2, 2): "122",
    }

def test_snafu_to_decimal(snafu_to_decimal_examples):

    decimals = {
        snafu: snafu_to_decimal(snafu)
        for snafu in snafu_to_decimal_examples.keys()
    }

    assert decimals == snafu_to_decimal_examples

def test_decimal_to_snafu(decimal_to_snafu_examples):

    snafus = {
        decimal: decimal_to_snafu(decimal)
        for decimal in decimal_to_snafu_examples.keys()
    }

    assert snafus == decimal_to_snafu_examples

def test_example_1(snafu_to_decimal_examples):

    decimal_sum = sum(
        int(snafu_to_decimal(snafu))
        for snafu in snafu_to_decimal_examples
    )
    assert decimal_sum == 4890

    snafu = decimal_to_snafu(str(decimal_sum))

    assert snafu == '2=-1=0'
