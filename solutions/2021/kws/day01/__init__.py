from pathlib import Path
from typing import List


def read_input(file: Path) -> List[int]:
    with open(file, 'rt') as f:
        lines = f.readlines()
    return [int(l) for l in lines]


def find_changes(values: List[int]) -> List[int]:
    return [value - values[ix] for ix, value in enumerate(values[1:])]


def count_increases(values):
    return [v for v in values if v > 0]


def sliding_sums(values):
    return [sum(values[ix:ix+3]) for ix, value in enumerate(values[2:])]
