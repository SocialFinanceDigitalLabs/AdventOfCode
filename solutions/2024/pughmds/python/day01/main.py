EXPECTED_TEST_ANSWER_PART1 = [11]
EXPECTED_TEST_ANSWER_PART2 = [31]


def parse_line(line: str) -> tuple[int, int]:
    """
    Turns a line of input into values that can be used.
    :param line: a line of data in the format SSSS     SSSS
    :return: data in the format with strings parsed to integers [NNNN,NNNN]
    """
    res = [int(i.strip()) for i in line.split()]
    return res[0], res[1]


def parse_data(data: list) -> list:
    """
    Turns a list of values and splits them into separate lists.
    Probably is unnecessary and the lists could be left as-is
    and still get the right answer, but this is more printable for
    testing/debugging
    :param data: The parsed data
    :return: data split into two lists in the format [[a],[b]]
    where a and b are the different distance lists in the input puzzle.
    """
    parsed_data = [[], []]
    for line in data:
        item1, item2 = parse_line(line)
        parsed_data[0].append(item1)
        parsed_data[1].append(item2)

    return parsed_data


def calculate_distances(list1: list, list2: list) -> list:
    """
    Work out the distances between two lists of equal size
    in the following way:
    * Consider two lists: [1,2,3] and [2,4,5]
    * Compare the smallest with the smallest (1-2) and return the absolute value
    * Compare the next smallest (2-4), then keep going until the last (3-5)

    :param list1: First list of input
    :param list2: Second list of numbers for input
    :return: a list of distances
    """
    distances = []
    if len(list1) != len(list2):
        raise "Lists need to be the same length!"

    for idx, d in enumerate(list1):
        distances.append(abs(list1[idx] - list2[idx]))
    return distances


def run(data: list) -> int:
    # Parse data into a list of locations
    locations = parse_data(data)

    # Sort the lists
    for idx, loc in enumerate(locations):
        locations[idx] = sorted(locations[idx])

    # Calculate the distance (absolute values)
    distances = calculate_distances(locations[0], locations[1])

    # The answer is the sum of the distances
    return sum(distances)


def calculate_similarity(list1, list2):
    """

    :param list1:
    :param list2:
    :param elem1:
    :param elem2:
    :return:
    """
    score = 0
    if len(list1) != len(list2):
        raise "Lists need to be the same length!"

    for item in list1:
        frequency = list2.count(item)
        score += frequency * item

    return score


def run_p2(data):
    # Parse data into a list of locations
    locations = parse_data(data)

    # Sort the lists
    for idx, loc in enumerate(locations):
        locations[idx] = sorted(locations[idx])

    score = calculate_similarity(locations[0], locations[1])

    # The answer is the sum of the distances
    return score
