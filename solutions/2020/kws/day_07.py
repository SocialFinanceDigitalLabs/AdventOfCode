#! /usr/bin/env python
import argparse
import re
import numpy as np

PTN_BAG_COLOR = re.compile(r"(.*) bags contain (.*)\.")
PTN_BAG_CONTENTS = re.compile(r"(\d+) (.*?) bag")


class Bag:

    def __init__(self, description, register):
        self.description = description
        self._register = register
        self.color, self.contains_description = Bag._parse_colour(self.description)
        self.contains = Bag._parse_contains(self.contains_description)

    def __str__(self):
        return f"{self.color}: {self.contains}"

    def __repr__(self):
        return self.__str__()

    @property
    def child_count(self):
        count = 0
        for c in self.contains:
            bag = self._register[c['color']]
            count += c['count'] * (bag.child_count + 1)
        return count

    @staticmethod
    def _parse_colour(description):
        """
        Extracts the colour and contents

        >>> Bag._parse_colour("bright white bags contain 1 shiny gold bag.")
        ('bright white', '1 shiny gold bag')

        >>> Bag._parse_colour("light red bags contain 1 bright white bag, 2 muted yellow bags.")
        ('light red', '1 bright white bag, 2 muted yellow bags')

        :param description:
        :return:
        """
        match = PTN_BAG_COLOR.match(description)
        return match.group(1), match.group(2)

    @staticmethod
    def _parse_contains(description):
        """
        Parse the contents so we can process them

        >>> Bag._parse_contains("1 shiny gold bag")
        [{'count': '1', 'colour': 'shiny gold'}]

        >>> Bag._parse_contains("1 bright white bag, 2 muted yellow bags")
        [{'count': '1', 'colour': 'bright white'}, {'count': '2', 'colour': 'muted yellow'}]

        :param description:
        :return:
        """
        groups = PTN_BAG_CONTENTS.finditer(description)
        return [dict(count=int(g[1]), color=g[2]) for g in groups]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 7 of Advent of Code 2020')
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
        rules = FILE.readlines()

    bags = {}
    for r in rules:
        b = Bag(r, bags)
        bags[b.color] = b

    inverted = {}
    for b in bags.values():
        for c in b.contains:
            inverted.setdefault(c['color'], []).append(b.color)

    colors = set(("shiny gold",))
    while True:
        added = 0
        for c in list(colors):
            for content in inverted.get(c, []):
                if content not in colors:
                    added += 1
                    colors.add(content)
        if added == 0:
            break

    print(len(colors)-1)

    print(bags['shiny gold'].child_count)


