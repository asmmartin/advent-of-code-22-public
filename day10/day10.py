# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring


class VideoSystem:
    def __init__(self, program: tuple[str]) -> None:
        # pylint: disable=invalid-name
        self.program = program
        self.X = 1
        self.clock = 0
        self.interesting_cycles = list(range(20, 221, 40))
        self.strong_signals = []
        self.CRT = [[' '] * 40 for _ in range(6)]


    @property
    def sprite_pixels(self):
        return (self.X - 1, self.X, self.X + 1)

    def run_program(self):
        for instruction in self.program:
            match instruction.split():
                case ['noop']:
                    self.noop()
                case ['addx', V] if V.lstrip('-').isdigit():
                    self.addx(int(V))

    def noop(self):
        self.clock_tick()

    def addx(self, V: int):
        self.clock_tick()
        self.clock_tick()
        self.X += V

    def clock_tick(self):
        self.draw_pixel()
        self.clock += 1
        if self.clock in self.interesting_cycles:
            self.strong_signals.append(self.X * self.clock)

    def _calculate_current_pixel_coords(self):
        return (self.clock // 40, self.clock % 40)

    def draw_pixel(self):
        row, col = self._calculate_current_pixel_coords()
        symbol = '#' if col in self.sprite_pixels else '.'
        self.CRT[row][col] = symbol

    def print_screen(self):
        for line in self.CRT:
            print(''.join(line))


def main():
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        program = input_file.read().splitlines()

    system = VideoSystem(program)
    system.run_program()
    strong_signal_total = sum(system.strong_signals)
    print(f'Strong signal total: {strong_signal_total}')

    print()
    system.print_screen()

if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    main()
