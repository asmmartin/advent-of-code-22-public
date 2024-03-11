# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from dataclasses import dataclass

def text_to_crate_stacks(input_text: str):

    stacks_text = input_text.splitlines()[:-1]
    stack_numbers = input_text.splitlines()[-1].split()

    number_of_stacks = int(stack_numbers[-1])

    crate_rows = parse_crate_rows(stacks_text, number_of_stacks)

    stacks = [list() for _ in range(number_of_stacks)]
    for crate_row in crate_rows:
        for stack_index, crate in enumerate(crate_row):
            if not crate:
                continue
            stacks[stack_index].append(crate)

    return stacks

def parse_crate_rows(stacks_text: str, number_of_stacks: int):
    crate_rows = []
    for stacks_text_line in stacks_text:
        crates_row = [
            stacks_text_line[i:i+4].strip()
            for i in range(0, len(stacks_text_line), 4)
        ]

        # For trimmed input files, add empty spaces
        while len(crates_row) < number_of_stacks:
            crates_row.append('')

        crate_rows.append(crates_row)

    return crate_rows[::-1]

@dataclass
class Instruction:
    amount: int
    origin: int
    destination: int

    @classmethod
    def from_string(cls, text: str):
        _, amount, _, origin, _, destination = text.split()
        return cls(
            amount=int(amount),
            origin=int(origin),
            destination=int(destination)
        )


class CrateMover9000:

    def execute(self, instruction: Instruction, stacks: list[list]):
        for _ in range(instruction.amount):
            crate = stacks[instruction.origin - 1].pop()
            stacks[instruction.destination - 1].append(crate)

class CrateMover9001:

    def execute(self, instruction: Instruction, stacks: list[list]):
        origin_stack = stacks[instruction.origin - 1]

        crates = origin_stack[-instruction.amount:]
        stacks[instruction.origin - 1] = origin_stack[:-instruction.amount]
        stacks[instruction.destination - 1].extend(crates)

def main():
    input_stacks_file = 'day5/input_crate_stacks.txt'
    input_instructions_file = 'day5/input_instructions.txt'

    with open(input_stacks_file, encoding='utf-8') as stacks_file:
        stacks_text = stacks_file.read()

    with open(input_instructions_file, encoding='utf-8') as instructions_file:
        instructions_text = instructions_file.read()

    instructions = [
        Instruction.from_string(text) for text in instructions_text.splitlines()
    ]

    stacks = text_to_crate_stacks(stacks_text)
    crane = CrateMover9000()
    for instruction in instructions:
        crane.execute(instruction, stacks)

    top_elements = [
        stack[-1] if stack else None
        for stack in stacks
    ]
    print(f'Top elements (CRATEMOVER9000): {top_elements}')

    stacks = text_to_crate_stacks(stacks_text)
    crane = CrateMover9001()
    for instruction in instructions:
        crane.execute(instruction, stacks)

    top_elements = [
        stack[-1] if stack else None
        for stack in stacks
    ]
    print(f'Top elements (CRATEMOVER9001): {top_elements}')

if __name__ == "__main__":
    main()
