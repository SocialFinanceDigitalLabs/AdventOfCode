# Advent of Code 2021 Day 22
import day22
from common import standard_setup


def main(*argv):
    lines = standard_setup(*argv)

    boxes = [day22.StateBox.from_input(day22.parse_input(line)) for line in lines]

    print(boxes)


if __name__ == "__main__":
    main()

