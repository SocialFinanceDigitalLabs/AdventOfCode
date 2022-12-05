from util import FileParser as BaseFileParser
import os
from typing import Iterable
from collections import defaultdict
from dataclasses import dataclass
import re

dir_path = os.path.dirname(os.path.realpath(__file__))


class FileParser(BaseFileParser):
    def load(self) -> list:
        with open(self.file_path) as f:
            data = f.read()
        return data


@dataclass
class Direction:
    origin: int
    destination: int
    count: int


def clean_stacks(stack_data: Iterable[str]) -> list[list[str]]:
    stack_data = stack_data.splitlines()
    stack_count = int(stack_data[-1].split()[-1])
    stack_data = stack_data[::-1][1:]
    stacks = defaultdict(list)
    for row in stack_data:
        idx = 0
        for s_idx in range(stack_count):
            cell = row[idx : idx + 3].strip("[] ") or None
            if cell:
                stacks[s_idx].append(cell)
            idx += 3 + 1
    return stacks


def clean_directions(directions_data: str) -> list[Direction]:
    directions = []
    for dir in directions_data.splitlines():
        nrs = re.findall(r"\d+", dir)
        directions.append(
            Direction(
                count=int(nrs[0]),
                origin=int(nrs[1]) - 1,
                destination=int(nrs[2]) - 1,
            )
        )
    return directions


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    stack_data, directions_data = data.split("\n\n")
    stacks = clean_stacks(stack_data)
    moves = clean_directions(directions_data)
    for move in moves:
        for _ in range(move.count):
            crate = stacks[move.origin].pop()
            stacks[move.destination].append(crate)
    
    return "".join([vals[-1] for vals in stacks.values()])


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    stack_data, directions_data = data.split("\n\n")
    stacks = clean_stacks(stack_data)
    moves = clean_directions(directions_data)
    for move in moves:
        crates = stacks[move.origin][-move.count:]
        stacks[move.origin] = stacks[move.origin][:-move.count]
        stacks[move.destination].extend(crates)

    return "".join([vals[-1] for vals in stacks.values()])


