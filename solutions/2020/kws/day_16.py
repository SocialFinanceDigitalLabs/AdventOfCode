#!/usr/bin/env python
import argparse
import re
from collections import namedtuple
import numpy as np


class Rule:
    """
    A ticket validation rule.

    >>> r = Rule("class: 1-3 or 5-7")
    >>> r
    Rule<class: 1-3 or 5-7>

    >>> r.is_valid(1)
    True

    >>> r.is_valid(0)
    False

    >>> r.is_valid(4)
    False

    >>> r.is_valid(7)
    True

    >>> r.is_valid(8)
    False

    """
    Range = namedtuple("Range", "min max")
    ptn = re.compile(r"([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)")

    def __init__(self, input_value: str):
        match = self.ptn.match(input_value)
        self.name = match.group(1)
        self.rules = (self.Range(
            int(match.group(2)),
            int(match.group(3))
        ), self.Range(
            int(match.group(4)),
            int(match.group(5)))
        )

    def __repr__(self):
        return f'Rule<{self.name}: {self.rules[0].min}-{self.rules[0].max} or {self.rules[1].min}-{self.rules[1].max}>'

    def is_valid(self, value):
        for r in self.rules:
            if r.min <= value <= r.max:
                return True

        return False


def parse_input(lines):
    """

    :param lines:
    :return:
    """

    rules = []
    my_ticket = []
    nearby_tickets = []
    current_ticket = None

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        elif line[0].isnumeric():
            current_ticket.append([int(v) for v in line.split(",")])
        elif line == "your ticket:":
            current_ticket = my_ticket
        elif line == "nearby tickets:":
            current_ticket = nearby_tickets
        else:
            rules.append(Rule(line))

    return rules, my_ticket, nearby_tickets


def find_field_errors(rules, tickets):
    invalid_values = []
    for t in tickets:
        for v in t:
            valid = False
            for r in rules:
                if r.is_valid(v):
                    valid = True
            if not valid:
                invalid_values.append(v)

    return invalid_values


def find_matching_rules(rules, ticket):
    matching_rules = {}
    for ix, v in enumerate(ticket):
        for r in rules:
            if r.is_valid(v):
                matching_rules.setdefault(ix, set()).add(r.name)

    return matching_rules


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 16 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'), nargs="?",
                        help='filename to your personal inputs', )
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    if args.test:
        import doctest

        doctest.testmod()
        print("Tests completed")
        exit(0)

    if args.file:
        with args.file as FILE:
            input_lines = FILE.readlines()

        rules, my_ticket, nearby_tickets = parse_input(input_lines)

        # Part 1
        invalid_values = find_field_errors(rules, nearby_tickets)
        print(f"Error scanning rate is {sum(invalid_values)}")

        # Part 2
        all_valid_rules = {}
        for t in nearby_tickets:
            valid_rules = find_matching_rules(rules, t)
            for k, v in valid_rules.items():
                all_valid_rules.setdefault(k, v)
                all_valid_rules[k] = all_valid_rules[k] & v

        matched_rules = {}
        longest_rule = 999
        while longest_rule > 0:
            longest_rule = 0
            for k, v in all_valid_rules.items():
                v = v - matched_rules.keys()
                if len(v) == 1:
                    matched_rules[v.pop()] = k
                    v = set()
                all_valid_rules[k] = v
                longest_rule = max(longest_rule, len(v))

        print("MATCHED RULES", matched_rules)

        my_ticket = my_ticket[0]
        ticket = {}
        for name, index in matched_rules.items():
                ticket[name] = my_ticket[index]

        print("MY TICKET", ticket)

        print("And the product of departure fields is", np.prod([v for k, v in ticket.items() if k.startswith("departure")]))

