import math
from functools import cached_property
from typing import Dict, List, Tuple

import click
import numpy as np
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit

SEGMENTS = (
    ("|", {"N", "S"}),
    ("-", {"E", "W"}),
    ("L", {"N", "E"}),
    ("J", {"N", "W"}),
    ("7", {"S", "W"}),
    ("F", {"S", "E"}),
)
connections = {k: v for k, v in SEGMENTS}


class Pipe:
    def __init__(self, x, y, char):
        self.pos = x, y
        self.char = char
        self.connections = set()
        self.level = None
        if char in connections:
            self.connections = connections[char]

    @cached_property
    def connected_tiles(self) -> Tuple[int, int]:
        x, y = self.pos
        tiles = []
        if "N" in self.connections:
            tiles.append((x, y - 1))
        if "S" in self.connections:
            tiles.append((x, y + 1))
        if "W" in self.connections:
            tiles.append((x - 1, y))
        if "E" in self.connections:
            tiles.append((x + 1, y))
        return tuple(tiles)

    def __repr__(self) -> str:
        return f"Pipe({self.char}{self.pos}, {self.connections})"


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day10(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day10.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day10.txt").read_text()

    input_data = input_data.splitlines()
    input_data = [list(line) for line in input_data]

    pipes = []
    for y, row in enumerate(input_data):
        for x, char in enumerate(row):
            if char == ".":
                continue
            else:
                pipe = Pipe(x, y, char)
                pipes.append(pipe)

    all_connections: Dict[tuple, List[Pipe]] = {}
    all_pipes = {p.pos: p for p in pipes}
    start = None

    for pipe in pipes:
        for c in pipe.connected_tiles:
            all_connections.setdefault(c, []).append(pipe)

        if pipe.char == "S":
            start = pipe

    # Get all the pipes that are connected to any of the pipes in loop_pipes
    def find_connections(loop_pipes, level):
        new_pipes = []
        for p in loop_pipes:
            new_pipes.extend([all_pipes.get(c) for c in p.connected_tiles])
        new_pipes = [p for p in new_pipes if p]
        new_pipes = [p for p in new_pipes if p.level is None]
        for p in new_pipes:
            p.level = level
        return new_pipes

    loop_pipes = all_connections[start.pos]
    for loop_pipe in loop_pipes:
        loop_pipe.level = 1

    new_pipes = loop_pipes
    loop_pipes = [start] + loop_pipes
    level = 2
    while new_pipes:
        new_pipes = find_connections(new_pipes, level)
        loop_pipes.extend(new_pipes)
        level += 1

    print(max([p.level for p in loop_pipes]))

    # F-7 = 2
    # F-J = 1

    # Part 2
    matrix = np.array(input_data)
    loop_coords = [p.pos for p in loop_pipes]
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if (x, y) not in loop_coords:
                matrix[y, x] = "."

    for y in matrix:
        print("".join(y))

    print("\n\n")

    inside_pieces = 0
    replacement_values = {"F": -0.5, "J": -0.5, "7": 0.5, "L": 0.5, "|": 1}
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if matrix[y, x] not in ".*":
                continue

            x_after = matrix[y, x:]
            x_values = [replacement_values.get(c, 0) for c in x_after]
            x_after_odd = math.floor(abs(sum(x_values))) % 2

            if x_after_odd:
                matrix[y, x] = " "
                inside_pieces += 1

    for y in matrix:
        print("".join(y))

    print(inside_pieces)
