import time
from collections import namedtuple
from contextlib import contextmanager
from math import floor
from typing import Iterable

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich import console
from rich.console import Group
from rich.live import Live
from rich.progress import track
from rich.text import Text


def noop(state, *_):
    yield


def addx(state, value):
    yield
    yield
    state.register_x += int(value)


class Communicator:
    def __init__(self):
        self.register_x = 1
        self.clock = 0
        self.operations = {
            "noop": noop,
            "addx": addx,
        }

    def run(self, command: str):
        op = command[:4]
        arg = command[4:]
        for _ in self.operations[op](self, arg):
            self.clock += 1
            yield


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day10(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day10.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day10.txt").read_text()

    input_data = input_data.splitlines()

    history = []
    comm = Communicator()
    history.append((comm.clock, comm.register_x))
    for command in input_data:
        for _ in comm.run(command):
            history.append((comm.clock, comm.register_x))

    cycles = [20, 60, 100, 140, 180, 220]
    print("Part 1:", sum([history[c][1] * c for c in cycles]))

    # Part 2
    pixel = 0
    display = []
    for h in history[1:]:
        sprite_pos = h[1]
        display_pos = (h[0] - 1) % 40
        cur_line = ["#" if abs(sprite_pos - i) < 2 else "." for i in range(40)]
        display.append(cur_line[display_pos])

    display = "".join(display)

    print("Part 2:")
    print(display[:40])
    print(display[40:80])
    print(display[80:120])
    print(display[120:160])
    print(display[160:200])
    print(display[200:240])
