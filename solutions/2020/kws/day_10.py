#!/usr/bin/env python
import argparse
from collections import Counter


class Node:
    """
    A representation of a node in the tree.
    The number of paths to this node is equal to the sum of the paths to each of the parents.
    """

    def __init__(self, value):
        self.value = value
        self.parents = set()
        self.paths = 0

    def __repr__(self):
        return f"{self.value}"

    def add_child(self, item):
        item.parents.add(self)

    def count(self):
        if len(self.parents) == 0:
            self.paths = 1
        else:
            self.paths = sum([p.paths for p in self.parents])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 10 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')

    args = parser.parse_args()

    with args.file as FILE:
        input_lines = FILE.readlines()

    input_lines = [int(i) for i in input_lines]
    input_lines.sort()
    input_lines = [0, *input_lines, max(input_lines) + 3]  ## Add start and finish

    gaps = [i - input_lines[ix] for ix, i in enumerate(input_lines[1:])]
    gap_counts = Counter(gaps)

    print("These are the gap counts:", gap_counts)

    print("The result for part 1 is:", gap_counts[1] * gap_counts[3])

    tree = {i: Node(i) for i in input_lines}
    for value, node in tree.items():
        for gap in [1, 2, 3]:
            next = tree.get(value + gap)
            if next is not None:
                node.add_child(next)

    for value in sorted(tree.keys()):
        node = tree[value]
        node.count()

    print("The result for part 2 is:", tree[max(tree.keys())].paths)
