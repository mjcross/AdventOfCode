from enum import Enum

class RPS(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    #               ROCK        PAPER       SCISSORS
    _beats =    (   SCISSORS,   ROCK,       PAPER   )
    _beatenby = (   PAPER,      SCISSORS,   ROCK    )

    @property
    def score(self):
        return RPS._scores.value[self.value]

    @property
    def beats(self):
        return RPS(RPS._beats.value[self.value])

    @property
    def beatenby(self):
        return RPS(RPS._beatenby.value[self.value])


def main():
    for turn in (RPS.ROCK, RPS.PAPER, RPS.SCISSORS):
        print(f'{turn.name} beats {turn.beats.name} but is beaten by {turn.beatenby.name}')


if __name__ == '__main__':
    main()
