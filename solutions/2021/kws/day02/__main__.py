import argparse
from pathlib import Path

from day02 import Submarine, Instruction

parser = argparse.ArgumentParser("Advent of Code - Day 2")
parser.add_argument("filename", type=str, help="The input filename")

args = parser.parse_args()

with open(Path(args.filename), 'rt') as file:
    lines = file.readlines()
lines = [l for l in lines if l != ""]

sub = Submarine()
for line in lines:
    sub.do(Instruction.from_string(line))

print(f"Submarine is now at {sub.pos} giving the product {sub.pos.x * sub.pos.d}")

sub = Submarine()
for line in lines:
    sub.do_with_aim(Instruction.from_string(line))

print(f"Submarine is now at {sub.pos} giving the product {sub.pos.x * sub.pos.d}")
