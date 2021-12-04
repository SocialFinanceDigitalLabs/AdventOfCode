import argparse
import inspect
import re
from typing import List


def standard_setup(*argv) -> List[str]:
    if len(argv) == 0:
        argv = None
    calling_module = get_calling_module_name()
    print(f"Welcome to Advent of Code Day {calling_module}")
    parser = argparse.ArgumentParser(f"Advent of Code - Day {calling_module}")
    parser.add_argument("filename", type=str, help="The input filename")
    args = parser.parse_args(argv)
    return file_to_lines(args.filename)


def file_to_lines(filename) -> List[str]:
    with open(filename, 'rt') as file:
        return file.readlines()


def get_calling_module_name() -> str:
    # Find day02 within a filename like 2021/kws/day04/__main__
    ptn = re.compile(r".*day(\d+).*")
    for frame in inspect.stack():
        if ptn.match(frame.filename):
            return int(ptn.match(frame.filename).group(1))
    return "unknown"
