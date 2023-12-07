import numpy as np
from itertools import compress

EXPECTED_TEST_ANSWER_PART1 = [288]
EXPECTED_TEST_ANSWER_PART2 = [71503]


def parse_line(line):
    strings = line.split()
    # Step 2: Filter out non-numeric words
    numeric_words = [word for word in strings if word.isdigit()]
    # Step 3: Convert numeric words to integers
    return [int(word) for word in numeric_words]


def run(data):
    times = parse_line(data[0])
    distances = parse_line(data[1])
    races = list(zip(times, distances))
    total = 1
    for time, distance in races:

        timings = np.arange(min(time, distance + 1))
        successes = timings[(time - timings) * timings > distance]

        total *= len(successes)

    return total


def run_p2(data):
    time = int(data[0].split(":")[1].replace(" ", ""))
    distance = int(data[1].split(":")[1].replace(" ", ""))

    # Takes about 2.096 seconds on puzzle input
    timings = np.arange(min(time, distance + 1))
    successes = timings[(time - timings) * timings > distance]

    '''
    # Takes about 11.725 seconds on puzzle input
    timings = range(min(time, distance + 1))
    condition = map(lambda t: (time - t) * t > distance, timings)
    successes = list(compress(timings, condition))
    '''

    '''
    # Takes about 7.733 seconds on puzzle input
    successes = [
        timing
        for timing in range(min(time, distance + 1))
        if timing * (time - timing) > distance
    ]
    '''

    return len(successes)
