#! /usr/bin/env python
import argparse
from typing import Iterable


def parse_trees(value: Iterable[str]):
    """
    Parses the input and returns the coordinates of all the trees.

    >>> parse_trees(["..##"])
    ({(2, 0), (3, 0)}, 4, 1)

    >>> parse_trees(["..##", ".#.#"])
    ({(3, 1), (1, 1), (2, 0), (3, 0)}, 4, 2)


    >>> parse_trees(["..##.......", "#...#...#.."])
    ({(0, 1), (8, 1), (2, 0), (3, 0), (4, 1)}, 11, 2)

    :param value:
    :return: set of tuple coordnates (x, y) or (c, r)
    """
    trees = set()
    max_col = 0
    max_row = 0
    for r_ix, row in enumerate(value):
        max_row = max(max_row, r_ix)
        for c_ix, col in enumerate(row):
            max_col = max(max_col, c_ix)
            if col == "#":
                trees.add((c_ix, r_ix))
    return trees, max_col + 1, max_row + 1


def check_for_tree(x, y, trees, max_x):
    """
    Checks to see if a tree exists in the given location, taking into account
    the infinite repeating pattern.

    >>> check_for_tree(0, 0, {(0, 0)}, 1)
    True

    >>> check_for_tree(0, 0, {(0, 1)}, 1)
    False

    >>> check_for_tree(15, 0, {(0, 0)}, 5)
    True

    :param x:
    :param y:
    :param trees:
    :param max_x:
    :return:
    """
    while x >= max_x:
        x -= max_x

    return (x, y) in trees


def check_slope(slope_x, slope_y, trees, max_x, max_y):
    y = 0
    x = 0
    route_trees = []
    while y <= max_y:
        y += slope_y
        x += slope_x
        has_tree = check_for_tree(x, y, trees, max_x)
        if has_tree:
            route_trees.append((x, y))

    return route_trees


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 3 of Advent of Code 2020')
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

    trees, max_x, max_y = parse_trees([v.strip() for v in values])

    route = check_slope(3, 1, trees, max_x, max_y)
    print(f"The solution to part 1 is {len(route)}")

    routes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = 1
    for r in routes:
        route = check_slope(r[0], r[1], trees, max_x, max_y)
        product *= len(route)

    print(f"The solution to part 2 is {product}")





