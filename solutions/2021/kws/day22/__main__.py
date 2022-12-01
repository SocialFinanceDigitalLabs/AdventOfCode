# Advent of Code 2021 Day 22
import day22
from common import standard_setup


def main(*argv):
    lines = standard_setup(*argv)

    boxes = [day22.StateBox.from_input(*day22.parse_input(line)) for line in lines]

    for b1 in boxes:
        intersects = 0
        for b2 in boxes:
            if b1 is not b2 and b1.intersects(b2):
                intersects += 1
        if intersects == 0:
            print(f"{b1} does not intersect with any other box")


if __name__ == "__main__":
    main()

