#! /usr/bin/env python
import argparse

from tqdm import tqdm


def get_parts(line):
    """
    Split each rule line into its constituent parts

    >>> get_parts('1-3 a: abcde')
    ('1-3 a', 'abcde')
    >>> get_parts('1-3 b: cdefg')
    ('1-3 b', 'cdefg')
    >>> get_parts('2-9 c: ccccccccc')
    ('2-9 c', 'ccccccccc')

    :param line:
    :return:
    """
    p1, p2 = line.split(":", 1)
    return p1.strip(), p2.strip()


def parse_rule(rule):
    """
    Parses the rule and returns a dict describing the rule

    >>> parse_rule('1-3 a')
    {'start': 1, 'end': 3, 'char': 'a'}
    >>> parse_rule('1-3 b')
    {'start': 1, 'end': 3, 'char': 'b'}
    >>> parse_rule('2-9 c')
    {'start': 2, 'end': 9, 'char': 'c'}
    >>> parse_rule('2-99 c')
    {'start': 2, 'end': 99, 'char': 'c'}

    :param rule: the rule string
    :return:
    """
    value_range, character = rule.split(' ')
    start, end = value_range.split('-')
    return dict(start=int(start), end=int(end), char=character)


def evaluate_sled_rental_rule(rule, input):
    """
    Evaluates each rule (as interpreted in part 1) against the input

    >>> evaluate_sled_rental_rule(dict(start=1, end=3, char='a'), 'abcde')
    True
    >>> evaluate_sled_rental_rule(dict(start=1, end=3, char='b'), 'cdefg')
    False
    >>> evaluate_sled_rental_rule(dict(start=2, end=9, char='c'), 'ccccccccc')
    True

    :param rule: an object describing the rule
    :param input: the input to check against
    :return:
    """

    count = input.count(rule['char'])
    return rule['start'] <= count <= rule['end']


def evaluate_corporate_rule(rule, input):
    """
    Evaluates each rule (as interpreted in part 2) against the input

    >>> evaluate_corporate_rule(dict(start=1, end=3, char='a'), 'abcde')
    True
    >>> evaluate_corporate_rule(dict(start=1, end=3, char='b'), 'cdefg')
    False
    >>> evaluate_corporate_rule(dict(start=2, end=9, char='c'), 'ccccccccc')
    False

    :param rule: an object describing the rule
    :param input: the input to check against
    :return:
    """

    input_for_test = input[rule['start']-1] + input[rule['end']-1]

    count = input_for_test.count(rule['char'])
    return count == 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 2 of Advent of Code 2020')
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

    valid_values = []
    with tqdm(values) as pbar:
        for v in pbar:
            pbar.desc = f"{v} ({len(valid_values)}"
            rule, input = get_parts(v)
            rule = parse_rule(rule)
            value = evaluate_sled_rental_rule(rule, input)
            if value:
                valid_values.append(input)

    print(f"There are {len(valid_values)} valid passwords in part 1")

    # Part 2

    valid_values = []
    with tqdm(values) as pbar:
        for v in pbar:
            pbar.desc = f"{v} ({len(valid_values)}"
            rule, input = get_parts(v)
            rule = parse_rule(rule)
            value = evaluate_corporate_rule(rule, input)
            if value:
                valid_values.append(input)

    print(f"There are {len(valid_values)} valid passwords in part 2")
