import re

EXPECTED_TEST_ANSWER_PART1 = [161]
EXPECTED_TEST_ANSWER_PART2 = [161, 48, 49]


def get_operations(input: str) -> list:
    """
    Uses regex to find all instances of the mul() command
    :param input: string to parse
    :return: a list of matches of the mul() command
    """
    matches = re.findall("mul\([0-9]+,[0-9]+\)", input)
    return matches


def parse_mul(input: str) -> int:
    """
    This takes a mul() comand and multiplies the numbers inside as instructed
    :param input: a string in the fomrat "mul(a,b)" where a and b are both numbers
    :return: The multiplication of both numbers found
    """
    input_values = input[3:].replace("(", "").replace(")", "").split(",")
    result = int(input_values[0]) * int(input_values[1])
    return result


def strip_out_missed_code(input: str) -> str:
    """
    This function removes do/don't pairs and any text in between them.
    The reason for this is so we can remove code we can safely ignore
    and then reuse the code created in part 1 to do the rest of the operations
    :param input: a string of commands
    :return: a string with any ignorable parts removed
    """
    # Find all do/don't pairs
    cleaned_input = re.sub(r"don't\(\)(.*?)do\(\)", "", input)

    # search for any trailing "don't()" functions without a matching do()
    cleaned_input = cleaned_input.split("don't()")[0]
    return cleaned_input


def run(data: list) -> int:
    score = 0
    for row in data:
        matches = get_operations(row)
        for m in matches:
            score += parse_mul(m)

    return score


def run_p2(data: list) -> int:
    score = 0
    # Part 2 is easier when we're working with a single string. So combine.
    data_string = "".join(data)

    # Clean the code and find any matches
    data_string = strip_out_missed_code(data_string)
    matches = get_operations(data_string)
    for m in matches:
        score += parse_mul(m)
    return score
