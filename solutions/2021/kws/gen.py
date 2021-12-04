#! /usr/bin/env python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser("Advent of Code")
parser.add_argument("day", type=int, help="The day to generate stubs for")

args = parser.parse_args()

module_name = f"day{args.day:02d}"
path = Path(module_name)

if path.exists():
    print(f"{path} already exists")
    exit(1)


def write_text_to_file(path, text):
    with open(path, "w") as f:
        f.write(text)


path.mkdir()

write_text_to_file(path / "__init__.py", f"# Advent of Code 2021 Day {args.day}\n\n\n")
write_text_to_file(path / "__main__.py", f"""# Advent of Code 2021 Day {args.day}
from common import standard_setup
import day{args.day:02d}


def main(*argv):
    lines = standard_setup(*argv)


if __name__ == "__main__":
    main()

""")
write_text_to_file(path / "sample_input.txt", "")

write_text_to_file(f"tests/test_day{args.day:02d}.py", f"""# Advent of Code 2021 Day {args.day}
import unittest
import day{args.day:02d}


class TestDay{args.day:02d}(unittest.TestCase):

    def test_parse_input(self):
        pass

""")
