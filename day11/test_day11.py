# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name


from functools import reduce
import pytest
from day11 import Monkey, Item, MonkeyTroop

TEXT_SAMPLES = (
'''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3''',
'''Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0''',
'''Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3''',
'''Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''
)

@pytest.fixture
def sample_monkeys():
    return [
        Monkey(0, [Item(79), Item(98)], lambda x: x * 19, lambda x: 3 if x % 23 else 2, divisor=23),
        Monkey(1, [Item(54), Item(65), Item(75), Item(74)], lambda x: x + 6, lambda x: 0 if x % 19 else 2, divisor=19),
        Monkey(2, [Item(79), Item(60), Item(97)], lambda x: x * x, lambda x: 3 if x % 13 else 1, divisor=13),
        Monkey(3, [Item(74)], lambda x: x + 3, lambda x: 1 if x % 17 else 0, divisor=17)
    ]

def test_item():
    assert Item(69).worry_level == 69

def test_monkey_from_text():
    monkeys = [Monkey.from_text(monkey_text) for monkey_text in TEXT_SAMPLES]

    assert all(monkeys[i] for i in range(4))

def test_monkey_id_from_text():
    monkey_ids = [Monkey.monkey_id_from_text(text) for text in TEXT_SAMPLES]
    assert monkey_ids == [0, 1, 2, 3]

def test_monkey_items_from_text():
    monkey_items = [
        Monkey.items_from_text(text) for text in TEXT_SAMPLES
    ]
    assert monkey_items == [
        [Item(79), Item(98)],
        [Item(54), Item(65), Item(75), Item(74)],
        [Item(79), Item(60), Item(97)],
        [Item(74)]
    ]

def test_monkey_operation_from_text():
    monkey_operations = [
      Monkey.operation_from_text(text) for text in TEXT_SAMPLES
    ]

    new_worry_levels = [
        operation(level) for operation, level in
        zip(monkey_operations, (79, 54, 79, 74))
    ]
    assert new_worry_levels == [1501, 60, 6241, 77]


def test_monkey_test_from_text():
    monkey_tests = [
      Monkey.test_from_text(text)[0] for text in TEXT_SAMPLES
    ]

    targets = [
        operation(level) for operation, level in
        zip(monkey_tests, (500, 20, 2080, 25))
    ]
    assert targets == [3, 0, 1, 1]

def test_monkey_examine_item(sample_monkeys):

    results = [monkey.examine_item() for monkey in sample_monkeys]
    assert results == [
        (Item(500),  3),
        (Item(20),   0),
        (Item(2080), 1),
        (Item(25),   1)
    ]
    for monkey in sample_monkeys:
        assert monkey.inspections_count == 1

def test_monkey_troop(sample_monkeys):

    troop = MonkeyTroop(monkeys=sample_monkeys)
    assert troop

def test_monkey_troop_process_rounds_one(sample_monkeys):

    troop = MonkeyTroop(monkeys=sample_monkeys)
    troop.process_rounds(1)

    worry_levels = [
        [item.worry_level for item in monkey.items]
        for monkey in troop.monkeys.values()
    ]
    assert worry_levels == [
        [20, 23, 27, 26],
        [2080, 25, 167, 207, 401, 1046],
        [],
        []
    ]

def test_monkey_troop_process_rounds_twenty(sample_monkeys):

    troop = MonkeyTroop(monkeys=sample_monkeys)
    troop.process_rounds(20)

    worry_levels = [
        [item.worry_level for item in monkey.items]
        for monkey in troop.monkeys.values()
    ]
    assert worry_levels == [
        [10, 12, 14, 26, 34],
        [245, 93, 53, 199, 115],
        [],
        []
    ]
    two_most_active = sorted(
        troop.monkeys.values(),
        key=lambda m: m.inspections_count,
        reverse=True
    )[:2]
    assert two_most_active[0].inspections_count * two_most_active[1].inspections_count == 10605

def test_monkey_troop_process_rounds_twenty_no_relief(sample_monkeys):

    divisor = reduce(
        lambda x, y: x * y,
        (monkey.divisor for monkey in sample_monkeys)
    )
    for monkey in sample_monkeys:
        monkey.relief_factor = 1
        monkey.modulo_normalizer = divisor
    troop = MonkeyTroop(monkeys=sample_monkeys)
    troop.process_rounds(20)

    two_most_active = sorted(
        troop.monkeys.values(),
        key=lambda m: m.inspections_count,
        reverse=True
    )[:2]
    assert two_most_active[0].inspections_count * two_most_active[1].inspections_count == 99 * 103

def test_monkey_troop_process_rounds_ten_thousand_no_relief(sample_monkeys):

    divisor = reduce(
        lambda x, y: x * y,
        (monkey.divisor for monkey in sample_monkeys)
    )
    for monkey in sample_monkeys:
        monkey.relief_factor = 1
        monkey.modulo_normalizer = divisor
    troop = MonkeyTroop(monkeys=sample_monkeys)
    troop.process_rounds(10000)

    two_most_active = sorted(
        troop.monkeys.values(),
        key=lambda m: m.inspections_count,
        reverse=True
    )[:2]
    assert two_most_active[0].inspections_count * two_most_active[1].inspections_count == 2713310158
