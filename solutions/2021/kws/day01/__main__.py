import argparse
from pathlib import Path

import day01

parser = argparse.ArgumentParser("Advent of Code - Day 1")
parser.add_argument("filename", type=str, help="The input filename")

args = parser.parse_args()

lines = day01.read_input(Path(args.filename))
changes = day01.find_changes(lines)
increases = day01.count_increases(changes)

print(f"{len(increases)} measurements were larger than the previous")

sliding = day01.sliding_sums(lines)
sliding_increases = day01.count_increases(day01.find_changes(sliding))

print(f"{len(sliding_increases)} sliding sums were larger than the previous")

