from aocd import get_data
from collections import namedtuple

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

signal_cycles = get_data(day=10, year=2022, session=session).splitlines()

test = [line.strip() for line in open(r"C:\Users\patrick.troy\Downloads\test.txt")]

X = 1
cycle = 0
signal_strength = 0


def calculate_signal_strength(cycle):
    for i in range(6):
        if cycle == 20 + 40 * i:
            global signal_strength
            signal_strength += X * cycle


for instruction in signal_cycles:
    elem = instruction.split()
    if elem[0] == "noop":
        cycle += 1
        calculate_signal_strength(cycle)
    if elem[0] == "addx":
        second_elem = int(elem[1])
        for value in range(2):
            cycle += 1
            calculate_signal_strength(cycle)
        X += second_elem

print(signal_strength)


def move_sprite(start_pos, move_by):
    if move_by == abs(move_by):
        line = "." * move_by + start_pos[:-move_by]
    else:
        line = start_pos[abs(move_by):] + "." * abs(move_by)
    assert len(start_pos) == len(line)
    return line


def current_crt_row(prev_row, i):
    global row
    if prev_row[i] == "#":
        row += "#"
    if prev_row[i] == ".":
        row += "."
    return row


start = "###....................................."
row = "#"
cycle = 0

for instruction in test:
    elem = instruction.split()
    if elem[0] == "noop":
        cycle += 1
    if elem[0] == "addx":
        second_elem = int(elem[1])
        current_crt_row(row, cycle)
        move_sprite(start, second_elem)
        current_crt_row(row, cycle)
        cycle += 1

print(row, len(row))

# for i in range(len(new)):
#     if start[i] == next[i]:
#         new += start[i]
#     else:
#         new += "."


