import re
from itertools import product
from itertools import combinations
from functools import lru_cache
from functools import cache
import random

EXPECTED_TEST_ANSWER_PART1 = [6, 21]
EXPECTED_TEST_ANSWER_PART2 = [6, 525152]


@lru_cache(maxsize=None)
def find_unequal_combinations(question_indices, num_hashes, input_string):
    possible_results = []
    input_string = list(input_string)
    possible_swap_indices = combinations(question_indices, num_hashes)
    for swap_group in possible_swap_indices:
        temp_list = list(input_string)
        for index in swap_group:
            temp_list[index] = "#"
        possible_results.append("".join(temp_list))
    return possible_results


def generate_combinations_with_hashes(input_string, num_hashes):
    # Find all indices of '?' characters in the input string
    question_indices = [index for index, char in enumerate(input_string) if char == "?"]
    question_count = len(question_indices)

    if num_hashes == question_count:
        return [input_string.replace("?", "#")]

    elif num_hashes > question_count:
        return []

    else:
        possible_results = find_unequal_combinations(
            tuple(question_indices), num_hashes, input_string
        )

    return [result.replace("?", ".") for result in possible_results]


@lru_cache(maxsize=None)
def extract_exact_groups(input_string):
    # Define a regular expression pattern to match groups of consecutive '#'
    pattern = re.compile(r"#+")

    # Use findall to extract all matches of the pattern in the input string
    groups = pattern.findall(input_string)

    return groups


def get_pattern_from_result(result):
    return [len(x) for x in result]


def check_row(row):
    total = 0
    if "?" not in row[0]:
        # This will be a simple check to see if making the pattern is possible
        result = extract_exact_groups(row[0])
        pattern = get_pattern_from_result(result)
        if pattern == row[1]:
            total += 1
    else:
        # Now we have to take into consideration the ? values...
        # '???.###'
        # How many ways could this match the pattern?
        num_to_find = sum(row[1]) - row[0].count("#")
        result = generate_combinations_with_hashes(row[0], num_to_find)

        # remove any non-matching results
        for test in result:
            groups = extract_exact_groups(test)
            group_size = get_pattern_from_result(groups)
            if group_size == row[1]:
                total += 1
    return total


def parse_lines(data, unfold_count=1):
    rows = []
    for line in data:
        record, pattern = line.strip().split(" ")
        pattern = pattern.split(",")
        pattern = [int(a) for a in pattern]
        if unfold_count > 1:
            newstring = '?'.join([record] * unfold_count)
        rows.append((newstring, pattern * unfold_count))
    return rows

@cache
def solve_recursively(input, groups):
    """
    We need a way to go through the more complex strings and
    solve it without actually storing anything other than if it works
    or not. Therefore, we can go through the string, left to right,
    recursivly checking to see if it matches the pattern
    """
    result = 0

    if not groups:
        if "#" in input:
            return 0
        else:
            return 1
    if not input:
        if not groups:
            return 1
        else:
            return 0

    if input[0] in ".?":
        result += solve_recursively(input[1:], groups)
    if input[0] in "#?":
        if (
            groups[0] <= len(input)
            and "." not in input[: groups[0]]
            and (groups[0] == len(input) or input[groups[0]] != "#")
        ):
            # If we have a series of # characters at the start, we can test a match
            result += solve_recursively(input[groups[0] + 1 :], groups[1:])

    return result


def run(data):
    """
    Manually go through and find the answer
    """
    rows = parse_lines(data)

    total = 0

    """for row in rows:
        total += check_row(row)"""

    for row in rows:
        # Let's try recursion!  (always a good idea with Python...)
        value = solve_recursively(row[0], row[1])
        total += value

    return total


def run_p2(data):
    """
    Once again, we have a solution that would blow up my old
    computer if we tried it with the extra inputs. Therefore,
    we need to do this more efficiently.
    """
    total = 0
    rows = parse_lines(data, 5)

    for row in rows:
        # Let's try recursion!  (always a good idea with Python...)
        #print(row)
        value = solve_recursively(row[0], tuple(row[1]))
        #print(value)
        total += value

    return total
