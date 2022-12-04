from enum import Enum

class RPS(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @property
    def score(self):
        return RPS._scores.value[self.value]

    @property
    def beats(self):
        return (RPS.SCISSORS, RPS.ROCK, RPS.PAPER)[self.value]

    @property
    def beatenby(self):
        return (RPS.PAPER, RPS.SCISSORS, RPS.ROCK)[self.value]


def main():
    for turn in RPS:
        print(f'{turn.name} beats {turn.beats.name} but is beaten by {turn.beatenby.name}')


if __name__ == '__main__':
    main()
