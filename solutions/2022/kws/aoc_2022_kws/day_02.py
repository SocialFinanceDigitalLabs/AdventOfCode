from enum import Enum

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config


class Hands(Enum):
    ROCK = 1, "SCISSORS"
    PAPER = 2, "ROCK"
    SCISSORS = 3, "PAPER"

    @property
    def beats(self) -> "Hands":
        return type(self)[self.value[1]]

    @property
    def looses_to(self) -> "Hands":
        for h in type(self):
            if h.beats_hand(self):
                return h

    @property
    def score(self):
        return self.value[0]

    def beats_hand(self, other: "Hands"):
        if self == other:
            return None
        return self.beats == other

    def __repr__(self):
        return f"<{type(self).__name__} {self.name}>"


codes = dict(
    A=Hands.ROCK,
    B=Hands.PAPER,
    C=Hands.SCISSORS,
    X=Hands.ROCK,
    Y=Hands.PAPER,
    Z=Hands.SCISSORS,
)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day02(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day02.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day02.txt").read_text()

    score = 0
    for line in input_data.splitlines():
        theirs, yours = line.split(" ")
        theirs = codes[theirs]
        yours = codes[yours]

        score += yours.score

        if yours.beats_hand(theirs) is None:
            score += 3
        elif yours.beats_hand(theirs):
            score += 6

    print(f"Part 1: {score}")

    # In the second part we interpret "yours" as strategy instead
    # of the actual hand. X = Lose, Y = Draw, Z = Win

    score = 0
    for line in input_data.splitlines():
        theirs, strategy = line.split(" ")
        theirs = codes[theirs]
        if strategy == "X":
            yours = theirs.beats
        elif strategy == "Y":
            yours = theirs
            score += 3
        elif strategy == "Z":
            yours = theirs.looses_to
            score += 6

        score += yours.score

    print(f"Part 2: {score}")
