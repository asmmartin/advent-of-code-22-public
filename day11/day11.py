# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from functools import reduce
from pathlib import Path
import re
from dataclasses import dataclass
from typing import Callable

@dataclass
class Item:
    worry_level: int


class Monkey:

    def __init__(
        self,
        monkey_id: int,
        items: list[Item],
        operation: Callable[[int], int],
        test: Callable[[int], int],
        divisor: int,
        relief_factor: int = 3
    ) -> None:
        self.monkey_id = monkey_id
        self.items = items
        self.operation = operation
        self.test = test
        self.relief_factor = relief_factor
        self.divisor = divisor
        self.inspections_count = 0
        self._modulo_normalizer = None

    @property
    def modulo_normalizer(self):
        return self._modulo_normalizer

    @modulo_normalizer.setter
    def modulo_normalizer(self, value: int):
        if self.relief_factor != 1:
            raise ValueError('Modulo arithm not available if there is relief factor!')
        self._modulo_normalizer = value
        return self

    def examine_item(self, index: int = 0) -> tuple[Item, int]:
        item = self.items.pop(index)
        worry_level = self.operation(item.worry_level)
        if not self._modulo_normalizer:
            item.worry_level = worry_level // self.relief_factor
        else:
            item.worry_level = worry_level % self._modulo_normalizer
        target = self.test(item.worry_level)
        self.inspections_count += 1
        return item, target

    @classmethod
    def from_text(cls, text: str) -> 'Monkey':
        text = text.strip()
        test, divisor = cls.test_from_text(text)
        return cls(
            monkey_id=cls.monkey_id_from_text(text),
            items=cls.items_from_text(text),
            operation=cls.operation_from_text(text),
            test=test,
            divisor=divisor
        )

    @staticmethod
    def monkey_id_from_text(text: str) -> int:
        monkey_id = re.search(r'Monkey (\d+):', text).group(1)
        return int(monkey_id)

    @staticmethod
    def items_from_text(text: str) -> int:
        worry_levels = re.search(
            r'Starting items: ((?:\d+(?:, )?)*)$',
            text,
            re.MULTILINE
        ).group(1)
        worry_levels = worry_levels.split(', ')
        return [Item(worry_level=int(level)) for level in worry_levels]

    @staticmethod
    def operation_from_text(text: str) -> Callable[[int], int]:

        operation_text = re.search(
            r'(?:Operation: new = )(.+)$',
            text,
            re.MULTILINE
        ).group(1)

        op1, operator, op2 = operation_text.split()
        def _operation(worry_level: int) -> int:
            value_1 = worry_level if op1 == 'old' else int(op1)
            value_2 = worry_level if op2 == 'old' else int(op2)
            if operator == '*':
                return value_1 * value_2
            else:
                return value_1 + value_2

        return _operation

    @staticmethod
    def test_from_text(text: str) -> Callable[[int], tuple[int]]:

        divisor = int(re.search(
            r'(?:Test: divisible by )(\d+)$',
            text,
            re.MULTILINE
        ).group(1))

        target_true = int(re.search(
            r'(?:If true: throw to monkey )(\d+)$',
            text,
            re.MULTILINE
        ).group(1))

        target_false = int(re.search(
            r'(?:If false: throw to monkey )(\d+)$',
            text,
            re.MULTILINE
        ).group(1))

        def _test(worry_level: int) -> int:

            if worry_level % divisor == 0:
                return target_true
            else:
                return target_false

        return _test, divisor

class MonkeyTroop:
    def __init__(self, monkeys: list[Monkey]) -> None:
        self.monkeys = {monkey.monkey_id: monkey for monkey in monkeys}

    def process_monkey_round(self, monkey: Monkey):
        while monkey.items:
            item, target = monkey.examine_item()
            self.monkeys[target].items.append(item)

    def process_rounds(self, amount: int):
        for _ in range(amount):
            for monkey in self.monkeys.values():
                self.process_monkey_round(monkey)

def main():
    input_text = Path(INPUT_FILE_PATH).read_text(encoding='utf-8')
    monkey_texts = input_text.split('\n\n')
    troop = MonkeyTroop(
        [Monkey.from_text(monkey_text) for monkey_text in monkey_texts]
    )
    troop.process_rounds(20)
    two_most_active = sorted(
        troop.monkeys.values(),
        key=lambda m: m.inspections_count,
        reverse=True
    )[:2]

    monkey_business = two_most_active[0].inspections_count * two_most_active[1].inspections_count
    print(f'The monkey business is {monkey_business}')

def main_2():
    input_text = Path(INPUT_FILE_PATH).read_text(encoding='utf-8')
    monkey_texts = input_text.split('\n\n')
    monkeys = [Monkey.from_text(monkey_text) for monkey_text in monkey_texts]

    divisor = reduce(
        lambda x, y: x * y,
        (monkey.divisor for monkey in monkeys)
    )
    for monkey in monkeys:
        monkey.relief_factor = 1
        monkey.modulo_normalizer = divisor

    troop = MonkeyTroop(monkeys)
    troop.process_rounds(10000)
    two_most_active = sorted(
        troop.monkeys.values(),
        key=lambda m: m.inspections_count,
        reverse=True
    )[:2]

    monkey_business = two_most_active[0].inspections_count * two_most_active[1].inspections_count
    print(f'The second monkey business is {monkey_business}')

if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    main()
    main_2()
