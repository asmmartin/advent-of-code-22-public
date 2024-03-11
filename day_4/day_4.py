# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

class SectionRange:
    def __init__(self, start: int, end: int) -> None:
        self.sections = set(range(start, end + 1 ))

    @classmethod
    def from_string(cls, section_range: str):
        start, end = section_range.split('-')
        start, end = int(start), int(end)
        return cls(start, end)

    def contains(self, other: 'SectionRange'):
        return self.sections.issuperset(other.sections)

    def calculate_intersection(self, other: 'SectionRange'):
        return self.sections.intersection(other.sections)

    def overlaps(self, other: 'SectionRange'):
        return not self.sections.isdisjoint(other.sections)

def main():
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        lines = tuple(line for line in input_file.read().splitlines() if line)

    range_pairs = []
    for line in lines:
        first, second = line.split(',')
        range_pairs.append((
            SectionRange.from_string(first),
            SectionRange.from_string(second)
        ))

    fully_overlapped_ranges_amount = 0
    for first, second in range_pairs:
        if first.contains(second) or second.contains(first):
            fully_overlapped_ranges_amount += 1

    print(f'Number of fully overlapped ranges: {fully_overlapped_ranges_amount}')

    overlapped_ranges_amount = 0
    for first, second in range_pairs:
        if first.overlaps(second):
            overlapped_ranges_amount += 1
    print(f'Number of overlapped ranges: {overlapped_ranges_amount}')

if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    main()
