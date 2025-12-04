from typing import Literal, NamedTuple

import click
from aoc_2025_kws.cli import main
from aoc_2025_kws.config import config
from aocd import submit


class Instruction(NamedTuple):
    direction: Literal["L", "R"]
    distance: int

    @property
    def step(self) -> int:
        return -1 if self.direction == "L" else 1

    @property
    def turns(self) -> range:
        return self.step * self.distance

    @classmethod
    def from_string(cls, string: str) -> "Instruction":
        direction = string[0]
        distance = int(string[1:])
        return cls(direction, distance)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day01(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day01.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day01.txt").read_text()

    instructions = [Instruction.from_string(line) for line in input_data.splitlines()]

    current_position = 50

    turns = {}
    for ix, instruction in enumerate(instructions):
        current_position += instruction.turns
        current_position = current_position % 100
        turns[ix] = current_position

    count_zero = sum(1 for turn in turns.values() if turn == 0)
    print(count_zero)

    if not sample:
        submit(count_zero, part="a", day=1, year=2025)

    current_position = 50

    passes_zero = 0

    for ix, instruction in enumerate(instructions):
        prev_position = current_position
        current_position += instruction.turns

        # We have to consider if we pass zero, stop on zero, or start on zero (in case we don't count the current zero)
        start_pos = prev_position + instruction.step

        # Rules were too confusing - doing it the hard way
        positions = list(range(start_pos, current_position, instruction.step)) + [
            current_position
        ]
        positions = [pos % 100 for pos in positions]
        passes_zero += sum(1 for pos in positions if pos == 0)

    total_passes = passes_zero
    print(total_passes)

    if not sample:
        submit(total_passes, part="b", day=1, year=2025)
