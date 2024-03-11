# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

import pytest

from day7 import parse_commands, CDCommand, LSCommand, FileElement, DirElement, FileSystem

@pytest.fixture
def example_input_lines():
    return [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k"
    ]

@pytest.fixture
def example_commands():
    return [
        CDCommand(target='/'),
        LSCommand(result=[
            DirElement(name='a'),
            FileElement(name='b.txt', size=14848514),
            FileElement(name='c.dat', size=8504156),
            DirElement(name='d'),
        ]),
        CDCommand(target='a'),
        LSCommand(result=[
            DirElement(name='e'),
            FileElement(name='f', size=29116),
            FileElement(name='g', size=2557),
            FileElement(name='h.lst', size=62596),
        ]),
        CDCommand(target='e'),
        LSCommand(result=[
            FileElement(name='i', size=584),
        ]),
        CDCommand(target='..'),
        CDCommand(target='..'),
        CDCommand(target='d'),
        LSCommand(result=[
            FileElement(name='j', size=4060174),
            FileElement(name='d.log', size=8033020),
            FileElement(name='d.ext', size=5626152),
            FileElement(name='k', size=7214296),
        ]),
    ]

@pytest.fixture
def example_file_system():
    file_system = FileSystem()
    file_system.directory_table = {
        '/': DirElement('/', sub_element_names=['a', 'b.txt', 'c.dat', 'd']),
            '/a': DirElement(name='a', sub_element_names=[
                'e', 'f', 'g', 'h.lst'
            ]),
                '/a/e': DirElement(name='e', sub_element_names=['i']),
                    '/a/e/i': FileElement(name='i', size=584),
                '/a/f': FileElement(name='f', size=29116),
                '/a/g': FileElement(name='g', size=2557),
                '/a/h.lst': FileElement(name='h.lst', size=62596),
            '/b.txt': FileElement(name='b.txt', size=14848514),
            '/c.dat': FileElement(name='c.dat', size=8504156),
            '/d': DirElement(name='d', sub_element_names=[
                'j', 'd.log', 'd.ext', 'k'
            ]),
                '/d/j': FileElement(name='j', size=4060174),
                '/d/d.log': FileElement(name='d.log', size=8033020),
                '/d/d.ext': FileElement(name='d.ext', size=5626152),
                '/d/k' : FileElement(name='k', size=7214296),
    }
    return file_system

def test_parse_commands(example_input_lines, example_commands):
    commands = parse_commands(example_input_lines)

    assert commands == example_commands

def test_filesystem_execute_commands(example_commands, example_file_system):

    file_system = FileSystem()
    for command in example_commands:
        command.execute(file_system)

    assert file_system.directory_table == example_file_system.directory_table

def test_update_dir_size(example_file_system):
    example_file_system.update_dir_size()
    example_sizes = {
        '/a/e': 584 ,
        '/a': 94853 ,
        '/d': 24933642,
        '/': 48381165,
    }
    for path, size in example_sizes.items():
        assert example_file_system.directory_table[path].size == size
