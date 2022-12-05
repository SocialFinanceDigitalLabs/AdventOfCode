from math import floor

EXPECTED_TEST_ANSWER_PART1 = "CMZ"
EXPECTED_TEST_ANSWER_PART2 = "MCD"

NUMBER_OF_STACKS = 9


def put_data_into_stacks(data):
    """
    Takes the row of data at the top of the input,
    works out how far in the letters are from the left-hand side
    and parses them into stacks
    """
    stacks = [[] for _ in range(NUMBER_OF_STACKS)]
    for rownum, row in enumerate(data):
        if row.strip() == "":
            return stacks, rownum
        else:
            for idx, item in enumerate(row):
                if (idx - 1) % 4 == 0 and item.strip() != "" and not item.isnumeric():
                    column = floor(idx / 4)
                    stacks[column].append(item)
    return None, None


def parse_instruction(instruction):
    """
    In the move instructions, pull out all the numbers and return
    the result in a more processing-friendly format
    """
    result = [int(s) for s in instruction.split() if s.isdigit()]
    return result[0], result[1] - 1, result[2] - 1


def get_answer(stacks):
    """
    Get the top item in each stack and make a string to be
    used as the "answer"
    """
    answer = []
    for stack in stacks:
        if len(stack) > 0:
            answer.append(stack[0])
    return "".join(answer)


def run(data):
    # Put input into stacks
    stacks, start_instructions_index = put_data_into_stacks(data)
    # Pick up where we left off as the rest of the input are move instructions
    for raw_instruction in data[start_instructions_index + 1:]:
        count, from_col, to_col = parse_instruction(raw_instruction)
        # Moving one item at a time is best done with pop/insert
        for move in range(1, count + 1):
            item = stacks[from_col].pop(0)
            stacks[to_col].insert(0, item)

    return get_answer(stacks)


def run_p2(data):
    # Put input into stacks
    stacks, start_instructions_index = put_data_into_stacks(data)
    # Pick up where we left off as the rest of the input are move instructios
    for raw_instruction in data[start_instructions_index + 1:]:
        count, from_col, to_col = parse_instruction(raw_instruction)
        # Since we're moving more than one item at a time, we can use slicing
        # There are likely more memory-efficient ways to do this...
        stacks[to_col] = stacks[from_col][:count] + stacks[to_col]
        stacks[from_col] = stacks[from_col][count:]

    return get_answer(stacks)
