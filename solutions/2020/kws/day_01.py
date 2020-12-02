#! /usr/bin/env python
import argparse
import itertools


def find_target(input, target=2020, combinations=2):
    """
    Finds 'combinations' numbers that add up to 2020

    Part 1:
    >>> find_target([1721, 979, 366, 299, 675, 1456])
    (1721, 299)

    Part 2:
    >>> find_target([1721, 979, 366, 299, 675, 1456], combinations=3)
    (979, 366, 675)

    :param input:
    :param target:
    :param combinations:
    :return:
    """

    for x in itertools.combinations(input, combinations):
        if sum(x) == 2020:
            return x


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 1 of Advent of Code 2020')
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
        values = FILE.readlines()

    values = [int(v) for v in values]

    v1, v2 = find_target(values)
    assert v1+v2 == 2020

    print(f"The answer to part 1 is {v1} * {v2} = {v1*v2}")

    v1, v2, v3 = find_target(values, combinations=3)
    assert v1+v2+v3 == 2020

    print(f"The answer to part 2 is {v1} * {v2} * {v3} = {v1*v2*v3}")

