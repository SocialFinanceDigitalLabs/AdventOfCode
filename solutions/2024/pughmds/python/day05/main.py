from typing import Tuple, List

EXPECTED_TEST_ANSWER_PART1 = [143]
EXPECTED_TEST_ANSWER_PART2 = [123]


def parse_input(data: list)-> Tuple[List[int], List[int]]:
    """
    This turns the expected input into integer values
    and we know half-way through the input there will
    be a blank line and the style will change.
    The first part determines the rules,
    the second part determines the updates
    :param data: A list of strings from the file input
    :return: Two lists. One contains the rules, the other
    the update instructions
    """
    ordering_rules = {}
    updates = []
    for row in data:
        row = row.strip()
        if "|" in row:
            values = row.strip().split("|")
            if int(values[0]) in ordering_rules.keys():
                ordering_rules[int(values[0])].append(int(values[1]))
            else:
                ordering_rules[int(values[0])] = [int(values[1])]
        elif "," in row:
            rule = [int(i) for i in row.split(",")]
            updates.append(rule)
        else:
            continue

    return ordering_rules, updates


def check_update(num: int, update: list, ordering_rules: dict)-> bool:
    """
    This checks an update is a "safe" one that
    follows all the rules
    :param num: The num we're checking is in the right place
    :param update: The entire update (the num belongs to)
    :param ordering_rules: The rules we need to follow
    :return: True or false to see if the update is "safe"
    """
    if num not in update:
        return True
    idx = update.index(num)
    trimmed_update = update[:idx]
    for test_value in ordering_rules[num]:
        if test_value in trimmed_update:
            return False
    return True


def find_middle(nums):
    if len(nums) % 2 == 0:
        return nums[int(len(nums) / 2 - 0.5)]
    else:
        return nums[int(len(nums) / 2)]


def check_num(update, ordering_rules, num):
    ordering_keys = ordering_rules.keys()
    if num not in ordering_keys:
        loc_idx = update.index(num)
        # This number doesn't have an ordering key, so should be at the end
        update = update[:loc_idx] + update[loc_idx + 1 :] + [update[loc_idx]]
    else:
        loc_idx = update.index(num)
        # Let's find numbers that aren't in the ordering rules by comparing sets
        out_of_order_nums = list(set(update[loc_idx + 1 :]) - set(ordering_rules[num]))
        # For each value that's out of order, let's move it before the number we're looking at.
        for v in out_of_order_nums:
            out_of_order_index = update.index(v)
            # Make sure the update has the list with the out of place number BEFORE the key number
            # As it's stated it should be in the rules.
            update = (
                update[:loc_idx]
                + [update[out_of_order_index]]
                + [update[loc_idx]]
                + update[loc_idx + 1 : out_of_order_index]
                + update[out_of_order_index + 1 :]
            )
    return update


def fix_updates(incorrect_updates, ordering_rules):
    for i in range(1, 10):
        # There are definitely a more efficent way to do this, but for speed I'm
        # Running the below algorithm a few times to clean up any missed values after rearranging.
        for idx, update in enumerate(incorrect_updates):
            # Looping over the incorrect updates,
            for num in update:
                incorrect_updates[idx] = check_num(update, ordering_rules, num)
    return incorrect_updates


def run(data):
    ordering_rules, updates = parse_input(data)
    print(ordering_rules)

    score = 0

    for update in updates:
        test_results = []
        for num in ordering_rules.keys():
            res = check_update(num, update, ordering_rules)
            if res:
                test_results.append(res)

        if len(test_results) == len(ordering_rules.keys()):
            # This update is correct and matches rules
            score += find_middle(update)
        else:
            # This update has some ordering issues...
            continue

    return score


def run_p2(data):
    # Just doing what was done in part 1 again...
    ordering_rules, updates = parse_input(data)

    score = 0
    incorrect_updates = []
    for update in updates:
        test_results = []
        for num in ordering_rules.keys():
            res = check_update(num, update, ordering_rules)
            if res:
                test_results.append(res)

        # Here is where we first change as we want the UNSAFE records
        if len(test_results) != len(ordering_rules.keys()):
            # This update has some ordering issues so we add it to a list
            incorrect_updates.append(update)

    incorrect_updates = fix_updates(incorrect_updates, ordering_rules)

    score = 0
    for i in incorrect_updates:
        v = find_middle(i)
        score += v

    return score


# 5353
