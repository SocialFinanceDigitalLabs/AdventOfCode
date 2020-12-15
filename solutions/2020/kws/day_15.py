#!/usr/bin/env python
import argparse

from collections import namedtuple

from tqdm import trange

Occurrence = namedtuple("Occurrence", "value current previous")

def last_index(mylist, myvalue):
    try:
        return mylist[::-1].index(myvalue) + 1
    except ValueError:
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 15 of Advent of Code 2020')
    parser.add_argument('puzzle_input', metavar='PUZZLE INPUT', type=str,
                        help='Your number sequence', )
    parser.add_argument('--turns', '-t', type=int, help='The number of turns to play', default=2020)

    args = parser.parse_args()

    numbers = args.puzzle_input.split(',')
    numbers = [int(n) for n in numbers]

    puzzle_sequence = {v: Occurrence(v, ix, None) for ix, v in enumerate(numbers)}

    last_number = puzzle_sequence.get(numbers[-1])
    for i in trange(len(puzzle_sequence), args.turns):
        seen_last = last_number.previous
        if seen_last is None:
            number = 0
        else:
            number = i - 1 - last_number.previous

        occ = puzzle_sequence.get(number)
        if occ is None:
            occ = None
        else:
            occ = occ.current

        last_number = Occurrence(number, i, occ)
        puzzle_sequence[number] = last_number

    print(last_number)
