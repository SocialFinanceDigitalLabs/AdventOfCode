import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config


def value(char: str) -> int:
    if char.islower():
        return ord(char) - 96
    else:
        return ord(char) - 38


class Bag:
    def __init__(self, value: str):
        self.c1 = value[0 : len(value) // 2]
        self.c2 = value[len(value) // 2 :]

    @property
    def common_chars(self):
        return set(self.c1) & set(self.c2)

    @property
    def common_score(self):
        return sum(value(c) for c in self.common_chars)

    @property
    def value(self):
        return self.c1 + self.c2


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day03(sample):
    data_folder = config.SAMPLE_DIR if sample else config.USER_DIR
    input_data = (data_folder / "day03.txt").read_text()
    bags = [Bag(line) for line in input_data.splitlines()]

    print("Part 1", sum([b.common_score for b in bags]))

    common_values = []
    for ix in range(0, len(bags), 3):
        common = set(bags[ix].value) & set(bags[ix + 1].value) & set(bags[ix + 2].value)
        common_values.append(common)

    print("Part 2", sum(value(list(c)[0]) for c in common_values))
