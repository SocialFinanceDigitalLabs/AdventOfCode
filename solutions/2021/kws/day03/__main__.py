import argparse
import sys
from pathlib import Path

import day03


def main(*argv):
    parser = argparse.ArgumentParser("Advent of Code - Day 3")
    parser.add_argument("filename", type=str, help="The input filename")
    args = parser.parse_args(argv)

    with open(Path(args.filename), 'rt') as file:
        lines = file.readlines()
    lines = [l for l in lines if l != ""]

    values = day03.input_to_array(lines)
    most_common = day03.most_common_value(values, keep=1)
    most_common_binary = day03.list_to_binary(most_common)

    print(f"The gamma rate is {most_common_binary} ({int(most_common_binary, 2)}) ")

    inverted = day03.invert(most_common)
    inverted_binary = day03.list_to_binary(inverted)

    print(f"The epsilon rate is {inverted_binary} ({int(inverted_binary, 2)}) ")

    print(f"The power consumption is {int(most_common_binary, 2) * int(inverted_binary, 2)}")


    oxygen_rating = day03.generator_rating(values, inverted=False)

    print(oxygen_rating)

    scrubber_rating = day03.generator_rating(values, inverted=True)

    print(scrubber_rating)

    print(f"The life support rating is "
          f"{int(day03.list_to_binary(oxygen_rating), 2) * int(day03.list_to_binary(scrubber_rating), 2)}")


if __name__ == "__main__":
    main(sys.argv)
