EXPECTED_TEST_ANSWER_PART1 = 157
EXPECTED_TEST_ANSWER_PART2 = 70

PRIORITIES = "abcdefghijklmnopqrstuvwxyz"


def split_list(list_to_split):
    """Takes a list and tries to split it exactly into two chunks"""
    c1 = list_to_split[: len(list_to_split) // 2]
    c2 = list_to_split[len(list_to_split) // 2 :]
    return c1, c2


def get_priorities_from_list(common_items):
    """
    Translates lists of items and determines their score / priorities
    """
    score = 0
    for item in common_items:
        if item in PRIORITIES:
            priority = PRIORITIES.index(item)
            score += priority + 1
        elif item in PRIORITIES.upper():
            priority = PRIORITIES.upper().index(item)
            score += priority + 27
    return score


def split_list_into_chunks(bag_contents, chunk_size):
    """
    Takes a list of items and groups them into chunks of equal size
    """
    for i in range(0, len(bag_contents), chunk_size):
        yield bag_contents[i: i + chunk_size]


def find_badge(group):
    """
    Takes the first element of the group and tries to find where they intersect with the other group members
    """
    common_elements = set(group[0]).intersection(*group)
    return list(set(common_elements))


def run(data):
    common = []
    for row in data:
        c1, c2 = split_list(row)
        common += list(set(c1).intersection(c2))
    score = get_priorities_from_list(common)
    return score


def run_p2(data):
    chunked_data = list(split_list_into_chunks(data, 3))
    badges = []
    for group in chunked_data:
        badges += find_badge(group)
    score = get_priorities_from_list(badges)
    return score
