#! /usr/bin/env python
import argparse
import re
import numpy as np


def to_binary_string(value):
    """
    Converts F or L to zeros, and B or R to 1 and interprets the string as a binary value

    >>> to_binary_string("FBFBBFF")
    ('0101100', 44)

    >>> to_binary_string("RLR")
    ('101', 5)

    :param value:
    :return:
    """
    value = re.sub(r"[FL]", "0", value)
    value = re.sub(r"[BR]", "1", value)
    return value, int(value, 2)


def get_seat_id(value):
    """
    Splits the string into row and column parts and interprets each as binary locations. Then
    multiplies the row by 8 and adds the column.

    >>> get_seat_id("FBFBBFFRLR")
    357
    >>> get_seat_id("BFFFBBFRRR")
    567
    >>> get_seat_id("FFFBBBFRRR")
    119
    >>> get_seat_id("BBFFBBFRLL")
    820

    :param value:
    :return:
    """
    row = to_binary_string(value[:7])
    col = to_binary_string(value[7:])
    return row[1]*8 + col[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 5 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    if args.test:
        import doctest

        doctest.testmod()

        print("Tests completed")
        exit(0)

    with args.file as FILE:
        file_content = FILE.readlines()

    seat_ids = [get_seat_id(line) for line in file_content]

    print(f"There are {len(seat_ids)} boardings cards in the the input, and the highest value is {np.max(seat_ids)}")

    for v in range(0, np.max(seat_ids)):
        if v not in seat_ids and v-1 in seat_ids and v+1 in seat_ids:
            print(f"The value {v} is not in the list, but {v-1} and {v+1} are")

