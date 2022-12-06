EXPECTED_TEST_ANSWER_PART1 = [7, 5, 6, 10, 11]
EXPECTED_TEST_ANSWER_PART2 = [19, 23, 23, 29, 26]


def run(data):
    message_size = 4
    for index in range(0, len(data[0]) - message_size):
        group = data[0][index : index + message_size]
        if len(list(set(group))) == message_size:
            return index + message_size
    return None


def run_p2(data):
    message_size = 14
    for index in range(0, len(data[0]) - message_size):
        group = data[0][index : index + message_size]
        if len(list(set(group))) == message_size:
            return index + message_size
    return None
