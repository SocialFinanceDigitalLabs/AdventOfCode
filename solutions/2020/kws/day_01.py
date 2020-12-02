#! /usr/bin/env python
import argparse
from tqdm import tqdm
from kws.aoc2020 import split_input


def find_target(input, target=2020):
    input.sort()

    pbar = tqdm(input)
    for v1 in pbar:
        for v2 in input[::-1]:
            pbar.desc = f"{v1} + {v2} = {v1+v2}"
            if v1+v2 == target:
                return v1, v2
            elif v1+v2 > target:
                continue


def find_three_target(input, target=2020):
    input.sort()

    pbar = tqdm(input)
    for v1 in pbar:
        for v2 in input[::-1]:
            for v3 in input[::-1]:
                pbar.desc = f"{v1} + {v2} + {v3} = {v1+v2+v3}"
                if v1+v2+v3 == target and v2 != v3:
                    return v1, v2, v3
            if v1+v2 > target:
                continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 1 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')

    args = parser.parse_args()

    with args.file as FILE:
        input = FILE.read()

    values = split_input(input, type=int)

    v1, v2 = find_target(values)
    assert v1+v2 == 2020

    print(f"The answer to part 1 is {v1} * {v2} = {v1*v2}")

    v1, v2, v3 = find_three_target(values)
    assert v1+v2+v3 == 2020

    print(f"The answer to part 1 is {v1} * {v2} * {v3} = {v1*v2*v3}")

