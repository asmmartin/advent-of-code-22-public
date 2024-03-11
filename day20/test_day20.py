# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest
from day20 import Node, EncryptedFile

def test_node():
    node_1 = Node(value=1)
    node_2 = Node(value=2, next=node_1)
    node_3 = Node(value=3, next=node_2, prev=node_1)

    assert node_3.next.next == node_1
    assert node_3.prev == node_1

def test_node_append():
    node_1 = Node(value=1)
    node_3 = Node(value=3)
    node_1.next = node_3
    node_3.prev = node_1

    node_2 = Node(value=2)
    node_1.append(node_2)

    assert node_1.next == node_2
    assert node_3.prev == node_2
    assert node_1.next.next == node_3
    assert node_3.prev.prev == node_1

def test_node_insert():

    node_1 = Node(value=1)
    node_3 = Node(value=3)
    node_1.next = node_3
    node_3.prev = node_1

    node_2 = Node(value=2)
    node_3.insert(node_2)

    assert node_1.next == node_2
    assert node_3.prev == node_2
    assert node_1.next.next == node_3
    assert node_3.prev.prev == node_1

def test_node_disappear():
    node_1 = Node(value=1)
    node_2 = Node(value=2)
    node_3 = Node(value=3)

    node_1.next = node_2
    node_2.next = node_3
    node_3.next = node_1

    node_3.prev = node_2
    node_2.prev = node_1
    node_1.prev = node_3

    node_2.disappear()

    assert node_1.next == node_3
    assert node_3.prev == node_1

def test_node_mix():
    node_1 = Node(value=1)
    node_2 = Node(value=2)
    node_3 = Node(value=3)
    node_4 = Node(value=-4)

    node_1.next = node_2
    node_2.next = node_3
    node_3.next = node_4
    node_4.next = node_1

    node_4.prev = node_3
    node_3.prev = node_2
    node_2.prev = node_1
    node_1.prev = node_4

    # Mix: [1, 2, 3, -4] -> [1, 3, -4, 2]
    node_2.mix(4)
    assert node_1.next == node_3 and node_3.prev == node_1
    assert node_2.prev == node_4 and node_2.next == node_1

    # Mix: [1, 3, -4, 2] -> [1, -4, 3, 2]
    node_4.mix(4)
    assert node_3.next == node_2 and node_2.prev == node_3
    assert node_4.next == node_3 and node_4.prev == node_1

def test_encrypted_file():
    numbers = [4, 5, 6, 1, 7, 8, 9]
    file = EncryptedFile(numbers)

    assert file.head.value == 4
    assert file.head.prev.value == 9
    assert file.head.next.next.next.value == 1
    assert file.head.next.next.next.next.next.next.next == file.head

    assert file.values == numbers

def test_encrypted_file_mix():
    numbers = [1, 2, -3, 3, -2, 0, 4]
    file = EncryptedFile(numbers)

    file.mix()

    assert file.values == [0, 3, -2, 1, 2, -3, 4]

def test_encrypted_file_coordinates():
    numbers = [1, 2, -3, 4, 0, 3, -2]
    file = EncryptedFile(numbers)

    coords = file.coordinates

    assert coords == (4, -3, 2)

def test_encrypted_file_decryption_key():

    numbers = [1, 2, -3, 3, -2, 0, 4]
    key = 811589153
    file = EncryptedFile(numbers, decryption_key=key)

    assert file.values == [
        0, 3246356612, 811589153, 1623178306, -2434767459,
        2434767459, -1623178306
    ]
