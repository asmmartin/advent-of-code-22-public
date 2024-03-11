# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from dataclasses import dataclass, field
from pathlib import PurePath

@dataclass
class Element:
    name: str
    size: int = 0


@dataclass
class DirElement(Element):
    sub_element_names: list[str] = field(default_factory=list)


@dataclass
class FileElement(Element):
    ...

class FileSystem:
    def __init__(self) -> None:
        self.pwd = PurePath('/')
        self.directory_table = {
            '/': DirElement('/')
        }

    def update_dir_size(self, dir_path: str = '/'):
        try:
            dir_to_update = self.directory_table[dir_path]
            if not isinstance(dir_to_update, DirElement):
                raise ValueError(f'{dir_path} is not a dir')
        except KeyError:
            raise ValueError(f'{dir_path} does not exist.') from None

        dir_to_update.size = 0
        for sub_element_name in dir_to_update.sub_element_names:
            sub_element_path = PurePath(dir_path).joinpath(sub_element_name)
            sub_element = self.directory_table[sub_element_path.as_posix()]
            if isinstance(sub_element, DirElement):
                self.update_dir_size(sub_element_path.as_posix())
            dir_to_update.size += sub_element.size

class Command:
    def execute(self, file_system: FileSystem): # pylint: disable=unused-argument
        ...

@dataclass
class CDCommand(Command):
    target: str

    def execute(self, file_system: FileSystem):
        match self.target:
            case '/':
                file_system.pwd = PurePath('/')
            case '..':
                file_system.pwd = file_system.pwd.parent
            case _:
                target_path = file_system.pwd.joinpath(self.target).as_posix()
                try:
                    target_dir = file_system.directory_table[target_path]
                    if not isinstance(target_dir, DirElement):
                        raise ValueError(f'cd error: {target_path} is not a dir')
                except KeyError:
                    raise ValueError(
                        f'cd error: {target_path} does not exist.') from None

                file_system.pwd = PurePath(target_path)

@dataclass
class LSCommand(Command):
    result: list[Element] = field(default_factory=list)

    def execute(self, file_system: FileSystem):
        current_dir = file_system.directory_table[file_system.pwd.as_posix()]
        for element in self.result:
            current_dir.sub_element_names.append(element.name)
            path = file_system.pwd.joinpath(element.name)
            file_system.directory_table[path.as_posix()] = element


def parse_commands(console_lines: list[str]) -> list[Command]:

    commands = []
    line_number = 0
    while line_number < len(console_lines):
        match console_lines[line_number].split():
            case ['$', 'cd', target]:
                commands.append(CDCommand(target=target))
                line_number += 1
            case ['$', 'ls']:
                command = LSCommand()
                line_number += 1

                while line_number < len(console_lines):
                    match console_lines[line_number].split():
                        case [size, name] if size.isdigit():
                            command.result.append(FileElement(name, int(size)))
                            line_number += 1
                        case ['dir', name]:
                            command.result.append(DirElement(name))
                            line_number += 1
                        case _:
                            break
                commands.append(command)
    return commands

def main():
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        console_lines = input_file.read().splitlines()

    commands = parse_commands(console_lines)
    file_system = FileSystem()
    for command in commands:
        command.execute(file_system)

    file_system.update_dir_size()

    dirs = [
        directory for directory in file_system.directory_table.values()
        if isinstance(directory, DirElement)
    ]

    small_dirs = [
        directory for directory in dirs
        if directory.size <= SMALL_DIRECTORY_THRESHOLD
    ]

    print('Total small dirs size:',
          sum(small_dir.size for small_dir in small_dirs)
    )

    unused_space = TOTAL_SPACE - file_system.directory_table['/'].size
    min_space_to_free = UPDATE_SPACE_REQUIRED - unused_space
    for directory in sorted(dirs, key=lambda d: d.size):
        if directory.size >= min_space_to_free:
            print(f'You should delete {directory.name} (size: {directory.size})')
            break

if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    SMALL_DIRECTORY_THRESHOLD = 100_000
    TOTAL_SPACE = 70_000_000
    UPDATE_SPACE_REQUIRED = 30_000_000
    main()
