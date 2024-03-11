# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import day13

SAMPLE_PAIRS = [
    ([1,1,3,1,1], [1,1,5,1,1]),
    ([[1],[2,3,4]], [[1],4]),
    ([9], [[8,7,6]]),
    ([[4,4],4,4], [[4,4],4,4,4]),
    ([7,7,7,7], [7,7,7]),
    ([], [3]),
    ([[[]]], [[]]),
    ([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
]

def test_compare():
    comparisons = [day13.compare(*pair) for pair in SAMPLE_PAIRS]
    assert comparisons == [-1, -1, 1, -1, 1, -1, 1, 1]

def test_calculate_right_indices_sum():

    comparisons = [-1, -1, 1, -1, 1, -1, 1, 1]
    right_indices_sum = day13.calculate_right_indices_sum(comparisons)

    assert right_indices_sum == 13

def test_pairs_parser():

    text = (
        '[1,1,3,1,1]\n'
        '[1,1,5,1,1]\n'
        '\n'
        '[[1],[2,3,4]]\n'
        '[[1],4]\n'
        '\n'
        '[9]\n'
        '[[8,7,6]]\n'
        '\n'
        '[[4,4],4,4]\n'
        '[[4,4],4,4,4]\n'
        '\n'
        '[7,7,7,7]\n'
        '[7,7,7]\n'
        '\n'
        '[]\n'
        '[3]\n'
        '\n'
        '[[[]]]\n'
        '[[]]\n'
        '\n'
        '[1,[2,[3,[4,[5,6,7]]]],8,9]\n'
        '[1,[2,[3,[4,[5,6,0]]]],8,9]'
    )
    pairs = day13.pairs_parser(text)
    assert pairs == SAMPLE_PAIRS

def test_sort_packets():

    packets = [packet for pair in SAMPLE_PAIRS for packet in pair]
    divider_packets = [ [[2]] , [[6]] ]
    packets += divider_packets
    ordered_packets = day13.sort_packets(packets)
    assert ordered_packets == [
        [],
        [[]],
        [[[]]],
        [1,1,3,1,1],
        [1,1,5,1,1],
        [[1],[2,3,4]],
        [1,[2,[3,[4,[5,6,0]]]],8,9],
        [1,[2,[3,[4,[5,6,7]]]],8,9],
        [[1],4],
        [[2]],
        [3],
        [[4,4],4,4],
        [[4,4],4,4,4],
        [[6]],
        [7,7,7],
        [7,7,7,7],
        [[8,7,6]],
        [9]
    ]

def test_calculate_decoder_key():

    divider_packets = [ [[2]] , [[6]] ]
    ordered_packets = [
        [],
        [[]],
        [[[]]],
        [1,1,3,1,1],
        [1,1,5,1,1],
        [[1],[2,3,4]],
        [1,[2,[3,[4,[5,6,0]]]],8,9],
        [1,[2,[3,[4,[5,6,7]]]],8,9],
        [[1],4],
        [[2]],
        [3],
        [[4,4],4,4],
        [[4,4],4,4,4],
        [[6]],
        [7,7,7],
        [7,7,7,7],
        [[8,7,6]],
        [9]
    ]

    assert day13.calculate_decoder_key(
        ordered_packets, divider_packets
    ) == 140
