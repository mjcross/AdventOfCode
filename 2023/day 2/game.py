from dataclasses import dataclass, field

@dataclass
class Turn:
    """Class to represent a turn of the game."""
    red: int = 0
    green: int = 0
    blue: int = 0

    def __gt__(self, other):
        return(
            self.red > other.red or
            self.green > other.green or
            self.blue > other.blue
        )

@dataclass
class Game:
    """Class to represent a game"""
    id: int
    turns: list = field(default_factory=list)