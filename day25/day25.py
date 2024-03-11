# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from pathlib import Path
from typing import Iterable


SNAFU_SYMBOLS_TO_INTS = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

INTS_TO_SNAFU_SYMBOLS = {v: k for k, v in SNAFU_SYMBOLS_TO_INTS.items()}

def snafu_to_decimal(snafu: str) -> str:

    snafu_ints = snafu_to_snafu_ints(snafu)

    return str(sum(
        snafu_int * 5**exponent
        for exponent, snafu_int in enumerate(snafu_ints[::-1])
    ))

def decimal_to_snafu(decimal: str) -> str:

    snafu_ints = []
    dividend = int(decimal)
    while dividend:
        dividend, remainder = dividend//5, dividend%5
        if remainder > 2:
            dividend, remainder = dividend + 1, remainder - 5
        snafu_ints.append(remainder)

    return snafu_ints_to_snafu(snafu_ints[::-1])


def snafu_to_snafu_ints(snafu: str) -> tuple[int, ...]:
    return tuple(
        SNAFU_SYMBOLS_TO_INTS[snafu_character]
        for snafu_character in snafu
    )

def snafu_ints_to_snafu(snafu_ints: Iterable[int]) -> str:
    return ''.join(
        INTS_TO_SNAFU_SYMBOLS[snafu_int]
        for snafu_int in snafu_ints
    )

def main_1(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    snafus = input_text.splitlines()

    decimal_sum = sum(
        int(snafu_to_decimal(snafu))
        for snafu in snafus
    )
    solution = decimal_to_snafu(str(decimal_sum))

    print(f'Solution part 1: {solution} ({decimal_sum=})')


if __name__ == "__main__":
    INPUT_FILE = './input.txt'
    main_1(INPUT_FILE)
