# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

OPERATION_FUNCTIONS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y,
    'noop': lambda *_: None
}

@dataclass
class Monkey:

    name: str
    family: dict[str, 'Monkey'] = field(default_factory=dict)
    operation_function: Callable[[int, int], int] = OPERATION_FUNCTIONS['noop']
    keys: tuple[str, str] | None = None
    result: int | None = None
    symbol: str = '='

    def __post_init__(self):
        self.family[self.name] = self

    def __call__(self) -> int:

        if self.result is not None:
            return self.result

        if not self.keys:
            raise ValueError('Yeller must not operate!')

        op1 = self.family[self.keys[0]]()
        op2 = self.family[self.keys[1]]()

        self.result = self.operation_function(op1, op2)
        return self.result

    def depends_on(self, other_name: str) -> bool:
        if self.name == other_name:
            return True

        if not self.keys:
            return False

        return (
            self.family[self.keys[0]].depends_on(other_name)
            or
            self.family[self.keys[1]].depends_on(other_name)
        )

    def simplify(self, variable: str) -> 'Monkey':

        if not self.depends_on(variable):
            self()
            return self

        if not self.keys:
            return self

        self.family[self.keys[0]].simplify(variable)
        self.family[self.keys[1]].simplify(variable)

        return self

    def solve(self, variable: str, target_result: int):

        if not self.depends_on(variable):
            raise ValueError(f'{self.name} does not depend on {variable}')

        if self.symbol == '=':
            if self.name != variable:
                raise ValueError(
                    'Error solving the equation: '
                    f'{variable}? -> {self.name} = {target_result}'
                )
            return target_result

        if not self.keys:
            raise ValueError(
                'Error solving the equation: '
                f'{variable}? -> {self.name} = {target_result}'
            )

        op1 = self.family[self.keys[0]].simplify(variable=variable)
        op2 = self.family[self.keys[1]].simplify(variable=variable)

        if op1.result is None and op2.result is None:
            raise ValueError(
                f'Cannot resolve for {self.name}. '
                f'Both parameters depend on {variable}'
            )

        try:
            if self.symbol == '+':
                if op1.depends_on(variable):
                    return op1.solve(
                        variable=variable,
                        target_result=target_result-op2.result # type: ignore
                    )
                return op2.solve(
                    variable=variable,
                        target_result=target_result-op1.result # type: ignore
                )
            elif self.symbol == '-':
                if op1.depends_on(variable):
                    return op1.solve(
                        variable=variable,
                        target_result=op2.result+target_result # type: ignore
                    )
                return op2.solve(
                    variable=variable,
                    target_result=op1.result-target_result # type: ignore
                )
            elif self.symbol == '*':
                if op1.depends_on(variable):
                    return op1.solve(
                        variable=variable,
                        target_result=target_result//op2.result # type: ignore
                    )
                return op2.solve(
                    variable=variable,
                    target_result=target_result//op1.result # type: ignore
                )
            elif self.symbol == '/':
                if op1.depends_on(variable):
                    return op1.solve(
                        variable=variable,
                        target_result=op2.result*target_result # type: ignore
                    )
                return op2.solve(
                    variable=variable,
                    target_result=op1.result//target_result # type: ignore
                )
            else:
                raise ValueError('Not valid operation')
        except ValueError as error:
            raise ValueError(
                'Error solving the equation: '
                f'{variable}? -> {self.name} = {target_result}'
            ) from error


    @classmethod
    def from_instruction(
        cls, instruction: str, family: dict[str, 'Monkey'],
    ) -> 'Monkey':
        fields = instruction.strip().split(':')
        name = fields[0]

        operation = fields[1].strip().split()
        if len(operation) == 1:
            return cls(
                name=name,
                result=int(operation[0]),
                family=family,
            )

        return cls(
            name=name,
            keys=(operation[0], operation[2]),
            operation_function=OPERATION_FUNCTIONS[operation[1]],
            symbol=operation[1],
            family=family
        )

def main_1(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    instructions = input_text.strip().splitlines()

    instructions = input_text.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)
    result = family['root']()

    print(f"Part 1 result: {result}")

def main_2(input_path: str):
    input_text = Path(input_path).read_text(encoding='utf-8')
    instructions = input_text.strip().splitlines()

    instructions = input_text.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    root = family['root']
    op1 = family[root.keys[0]]
    op2 = family[root.keys[1]]

    root.simplify('humn')

    if op1.depends_on('humn'):
        result = op1.solve(target_result=op2.result, variable='humn')
    else:
        result = op2.solve(target_result=op1.result, variable='humn')

    print(f'Part 2 result: {result}')

if __name__ == "__main__":
    INPUT_FILE = './input.txt'
    main_1(INPUT_FILE)
    main_2(INPUT_FILE)
