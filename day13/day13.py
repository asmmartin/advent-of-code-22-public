
import json
from math import prod
import sys
from functools import cmp_to_key

ElementToCompare = int | list['ElementToCompare']

def compare(left: ElementToCompare, right: ElementToCompare) -> int:

    match left, right:
        case int(), int() :
            if left < right:
                return -1
            elif left > right:
                return 1
            return 0

        case list(), list():
            max_size = max(len(left), len(right))
            for index in range(max_size):
                try:
                    left_element = left[index]
                except IndexError:
                    return -1
                try:
                    right_element = right[index]
                except IndexError:
                    return 1

                result = compare(left_element, right_element)
                if result != 0:
                    return result
            return 0

        case list(), int():
            return compare(left, [right])

        case int(), list():
            return compare([left], right)

def calculate_right_indices_sum(comparison_results: list[int]) -> int:
    in_order_results = [
        index for index, value in enumerate(comparison_results) if value != 1
    ]
    return sum(in_order_results) + len(in_order_results)

def pairs_parser(text: str) -> list[tuple[ElementToCompare, ElementToCompare]]:
    pairs_texts = text.split('\n\n')
    pairs = []
    for pair_text in pairs_texts:
        left, right = pair_text.splitlines()
        pairs.append((json.loads(left), json.loads(right)))
    return pairs

def sort_packets(packets: list[ElementToCompare]) -> list[ElementToCompare]:
    return sorted(
        packets,
        key=cmp_to_key(compare)
    )

def calculate_decoder_key(
    packets: list[ElementToCompare],
    divider_packets: list[ElementToCompare]
) -> int:
    return prod([
        packets.index(divider_packet) + 1
        for divider_packet in divider_packets
    ])


def main():
    pairs = pairs_parser(sys.stdin.read())
    comparisons = [compare(*pair) for pair in pairs]
    in_order_indices_sum = calculate_right_indices_sum(comparisons)
    print(f'The sum is {in_order_indices_sum}')

    packets = [packet for pair in pairs for packet in pair]
    divider_packets = [ [[2]] , [[6]] ]
    packets += divider_packets
    ordered_packets = sort_packets(packets)
    decoder_key = calculate_decoder_key(ordered_packets, divider_packets)
    print(f'The decoder key is {decoder_key}')


if __name__ == "__main__":
    main()
