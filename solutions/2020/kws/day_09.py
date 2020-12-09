#! /usr/bin/env python
import argparse

from tqdm import tqdm

import kws.bootcode as bc


def find_sums(number, preamble):
    """
    Returns all matching sums from the preamble.

    >>> find_sums(26, range(1,26))
    {(5, 21), (3, 23), (4, 22), (6, 20), (7, 19), (12, 14), (10, 16), (11, 15), (8, 18), (9, 17), (1, 25), (2, 24)}
    >>> find_sums(49, range(1,26))
    {(24, 25)}
    >>> find_sums(100, range(1,26))
    set()
    >>> find_sums(50, range(1,26))
    set()

    :param number:
    :param preamble:
    :return:
    """

    results = set()
    for a in preamble:
        b = number - a
        if a != b and b in preamble:
            results.add((min(a, b), max(a, b)))
    return results


def extract_number_and_preamble(index, sequence, preamble_length=25):
    """
    Extracts the number given by the sequence, as well as the preamble.

    >>> extract_number_and_preamble(25, list(range(1,26))+[46])
    (46, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])

    >>> extract_number_and_preamble(5, list(range(1,26))+[46], preamble_length=5)
    (6, [1, 2, 3, 4, 5])

    :param index:
    :param sequence:
    :param preamble_length:
    :return:
    """
    number = sequence[index]
    start = max(0, index-preamble_length)
    preamble = sequence[start:start+preamble_length]
    return number, preamble


def find_range_sums(target, sequence):
    """
    Finds the first sum of contiguous numbers that add up to the target.

    >>> find_range_sums(5, list(range(1,10)))
    [2, 3]

    >>> find_range_sums(9, list(range(1,10)))
    [2, 3, 4]

    >>> find_range_sums(11, list(range(1,10)))
    [5, 6]

    >>> find_range_sums(26, list(range(1,10)))
    [5, 6, 7, 8]

    >>> find_range_sums(24, list(range(1,10)))
    [7, 8, 9]

    :param target:
    :param sequence:
    :return:
    """
    for seq_start in range(0, len(sequence)+1):
        for seq_len in range(seq_start+1, len(sequence)+1):
            if sum(sequence[seq_start:seq_len]) == target:
                return sequence[seq_start:seq_len]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 9 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--length', '-l', type=int, default=25, help="The preamble length")

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
        print("Tests completed")
        exit(0)

    with args.file as FILE:
        input_lines = FILE.readlines()

    input_lines = [int(n) for n in input_lines]

    for ix in range(args.length, len(input_lines)):
        number, preamble = extract_number_and_preamble(ix, input_lines, preamble_length=args.length)
        sums = find_sums(number, preamble)
        if len(sums) == 0:
            first_invalid = number
            break

    print(f"The first invalid number in the sequence is {first_invalid}")

    addends = find_range_sums(first_invalid, input_lines)

    print(f"The encryption weakness is {min(addends) + max(addends)}")