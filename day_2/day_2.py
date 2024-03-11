# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from enum import Enum

class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_str_one(cls, shape_str: str):
        shape_reprs = {
            'A': cls.ROCK,
            'B': cls.PAPER,
            'C': cls.SCISSORS,
            'X': cls.ROCK,
            'Y': cls.PAPER,
            'Z': cls.SCISSORS,
        }
        return shape_reprs[shape_str]

    @classmethod
    def from_str_pair(cls, opponent_shape_str: str, desired_result: str):
        opponent = cls.from_str_one(opponent_shape_str)
        if desired_result == 'X':
            mine_dict = {
                'A': cls.SCISSORS,
                'B': cls.ROCK,
                'C': cls.PAPER,
            }
        elif desired_result == 'Y':
            mine_dict = {
                'A': cls.ROCK,
                'B': cls.PAPER,
                'C': cls.SCISSORS,
            }
        else:
            mine_dict = {
                'A': cls.PAPER,
                'B': cls.SCISSORS,
                'C': cls.ROCK,
            }

        mine = mine_dict[opponent_shape_str]
        return opponent, mine

class Game:

    def __init__(self, str_repr: str) -> None:
        opponent, mine = str_repr.split()
        self.opponent, self.mine = Shape.from_str_pair(opponent, mine)

    @property
    def score(self):
        _score = 0

        # Outcome
        if self.opponent == self.mine:
            _score += 3
        elif (self.opponent, self.mine) in (
            (Shape.ROCK, Shape.PAPER),
            (Shape.PAPER, Shape.SCISSORS),
            (Shape.SCISSORS, Shape.ROCK)
        ):
            _score += 6

        # Shape value
        _score += self.mine.value

        return _score

def parse_strategy(input_file_path: str):
    game_reprs = read_input_lines(input_file_path)
    games = [Game(game_repr) for game_repr in game_reprs]
    return games

def read_input_lines(input_file_path: str):
    with open(input_file_path, encoding='utf-8') as input_file:
        data = input_file.read()
        return [line for line in data.splitlines() if line]

if __name__ == "__main__":
    INPUT_PATH = 'input.txt'
    strategy = parse_strategy(INPUT_PATH)
    total_score = sum(game.score for game in strategy)
    print(f'Total score for {len(strategy)} games is: {total_score}')
