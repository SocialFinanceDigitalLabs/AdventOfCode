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


def parse_moves(input_data):
    for line in input_data.splitlines():
        direction, distance = line.split(" ", 1)
        for _ in range(int(distance)):
            yield direction


def sign(x: int):
    return -1 if x < 0 else 1


class Knot:
    def __init__(self, name="knot"):
        self.name = name
        self.x = 0
        self.y = 0

    def move(self, direction):
        if direction == "U":
            self.y -= 1
        elif direction == "D":
            self.y += 1
        elif direction == "L":
            self.x -= 1
        elif direction == "R":
            self.x += 1
        else:
            raise ValueError(f"Unknown direction {direction}")

    def move_towards(self, knot: "Knot"):
        dx = knot.x - self.x
        dy = knot.y - self.y
        if abs(dx) <= 1 and abs(dy) <= 1:
            return
        elif abs(dx) >= 1 and abs(dy) >= 1:
            self.x += sign(dx)
            self.y += sign(dy)
        elif abs(dx) >= 1:
            self.x += sign(dx)
        elif abs(dy) >= 1:
            self.y += sign(dy)
        else:
            raise ValueError("I'm lost!")

    @property
    def pos(self):
        return self.x, self.y

    def __repr__(self):
        return f"Knot({self.x}, {self.y})"


def render_map(dx, dy, rope, visited):
    head = rope[0]
    rope_pos = {(0, 0): Knot("s")} | {(knot.x, knot.y): knot for knot in rope[::-1]}

    hx = dx * floor(abs(head.x) / dx) * sign(head.x)
    hy = dy * floor(abs(head.y) / dy) * sign(head.y)

    y0, y1, x0, x1 = hy - dy, hy + dy, hx - dx, hx + dx

    rows = []
    for y in range(y0, y1 + 1):
        row = [(f"{y:03d}", "green")]
        for x in range(x0, x1 + 1):
            k = rope_pos.get((x, y))
            if k == head:
                color = "bold yellow"
            elif (x, y) == (0, 0):
                color = "bold green"
            else:
                color = "red"
            row.append((k.name, color) if k else ("#" if (x, y) in visited else "."))
        rows += row
        rows.append("\n")

    x_axis = [f"{x:03d}" for x in range(x0, x1 + 1)]
    for i in range(3):
        rows.append("   ")
        rows.append(("".join([x[i] for x in x_axis]), "green"))
        rows.append("\n")

    return Text.assemble(*rows)


@contextmanager
def show_map(dx, dy):
    visited = set()
    with Live() as live:

        def display(rope):
            t = render_map(dx, dy, rope, visited)
            live.update(t)
            visited.add(rope[-1].pos)

        yield display


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--animate", "-a", is_flag=True)
@click.option("--fps", type=int, default=10)
def day09(sample, animate, fps):
    if sample:
        input_data = (config.SAMPLE_DIR / "day09.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day09.txt").read_text()

    move_list = list(parse_moves(input_data))
    head = Knot("H")
    tail = Knot("T")

    positions = [tail.pos]
    with show_map(50, 25) as display:
        for move in move_list:
            head.move(move)
            tail.move_towards(head)
            positions.append(tail.pos)
            if animate:
                display([head, tail])
                time.sleep(1 / fps)

    print("Part 1", len(set(positions)))

    if sample:  # We use a longer sample input for part 2
        input_data = (config.SAMPLE_DIR / "day09_2.txt").read_text()
        move_list = list(parse_moves(input_data))

    head = Knot("H")
    tail = Knot("9")
    rope = [head] + [Knot(str(_)) for _ in range(8)] + [tail]
    assert len(rope) == 10

    positions = [tail.pos]

    with show_map(50, 25) as display:
        for move in move_list:
            head.move(move)
            for ix, knot in enumerate(rope[1:]):
                knot.move_towards(rope[ix])
            positions.append(tail.pos)
            if animate:
                display(rope)
                time.sleep(1 / fps)

    print("Part 2", len(set(positions)))
