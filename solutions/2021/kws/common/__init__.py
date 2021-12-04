import argparse
import inspect
from typing import List


def standard_args(day: int, *argv):
    parser = argparse.ArgumentParser(f"Advent of Code - Day {day}")
    parser.add_argument("filename", type=str, help="The input filename")
    return parser.parse_args(argv)


def file_to_lines(filename) -> List[str]:
    with open(filename, 'rt') as file:
        return file.readlines()