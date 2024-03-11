# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

from pathlib import Path
from typing import Self


class Node:

    def __init__(
        self,
        value: int,
        prev: Self | None = None,
        next: Self | None = None # pylint: disable=redefined-builtin
    ):
        self.value = value
        self.prev = prev if prev is not None else self
        self.next = next if next is not None else self

    def append(self, next_node: Self) -> Self:
        """Append a node after this one. Returns the appended node"""

        next_node.next = self.next
        next_node.prev = self
        self.next.prev = next_node
        self.next = next_node

        return next_node

    def insert(self, previous_node: Self) -> Self:
        """Insert a node before this one. Returns the inserted node"""

        previous_node.next = self
        previous_node.prev = self.prev
        self.prev.next = previous_node
        self.prev = previous_node

        return previous_node

    def disappear(self):
        """Disappear from the next and prev Nodes"""

        self.next.prev, self.prev.next = self.prev, self.next

    def mix(self, list_length: int):
        """Move through the list *self.value* positions"""

        steps = self.value % (list_length - 1)
        if steps == 0:
            return

        self.disappear()
        cursor = self

        for _ in range(steps):
            cursor = cursor.next
        cursor.append(self)

class EncryptedFile:

    def __init__(self, values: list[int], decryption_key: int = 1):
        if not values:
            raise ValueError('Needed at least 1 value!')

        values = [value * decryption_key for value in values]

        self.head = Node(value=values[0])
        self.original_order = [self.head]

        tail = self.head
        for value in values[1:]:
            new_node = Node(value=value)
            tail = tail.append(new_node)
            self.original_order.append(new_node)
            if value == 0:
                self.head = new_node

    def __len__(self) -> int:
        return len(self.original_order)

    @property
    def values(self) -> list[int]:
        values = []
        cursor = self.head
        for _ in range(len(self)):
            values.append(cursor.value)
            cursor = cursor.next
        return values

    @property
    def coordinates(self) -> tuple[int, ...]:
        coordinates: list[int] = []
        cursor = self.head
        for _ in range(3):
            for _ in range(1000):
                cursor = cursor.next
            coordinates.append(cursor.value)
        return tuple(coordinates)

    def mix(self):
        for node in self.original_order:
            node.mix(len(self))

def main(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    numbers = [int(number) for number in input_text.splitlines()]

    encrypted_file = EncryptedFile(numbers)
    encrypted_file.mix()

    print('Part 1:')
    print(f'{encrypted_file.coordinates=}. Sum: {sum(encrypted_file.coordinates)}')
    print('-----------------------')

def main_2(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    numbers = [int(number) for number in input_text.splitlines()]
    encryption_key = 811589153
    encrypted_file = EncryptedFile(numbers, encryption_key)

    for _ in range(10):
        encrypted_file.mix()

    print('Part 2:')
    print(f'{encrypted_file.coordinates=}. Sum: {sum(encrypted_file.coordinates)}')

if __name__ == "__main__":
    INPUT_FILE = './input.txt'
    main(INPUT_FILE)
    main_2(INPUT_FILE)
