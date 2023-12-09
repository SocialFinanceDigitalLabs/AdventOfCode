# First attempt: worked great for part 1, but too slow for part 2 (it'd take 3.5 days to get an answer on my
# really old personal computer). This is a brute-force method. It'd get the job done, but take forever. There
# are faster ways to do this, such as using the mapping functions.

EXPECTED_TEST_ANSWER_PART1 = [35]
EXPECTED_TEST_ANSWER_PART2 = [46]

import re
import numpy as np


def parse_maps(maps):
    map_pipe = {}

    for i, map_values in enumerate(maps):
        values = map_values.split("\n")[1:]
        for map_val in values:
            if not map_val:
                continue
            input_data = list(map(int, map_val.split()))
            drs, srs, rl = input_data
            if i not in map_pipe:
                map_pipe[i] = []
            map_pipe[i].append(
                {"dest_range_start": drs, "source_range_start": srs, "range_length": rl}
            )

    return map_pipe


def parseInput(data):
    # This is one of those programs that would have been easier to handle by taking the entire input
    # file as one string and splitting from there. Because I don't want to rewrite my shared input script
    # We can just combine it back here:
    instructions_text = "\n".join(data)

    # This should roughly split the text into sections
    sections = re.split(r"\n\s*\n", instructions_text)
    seeds = sections[0].split(":")[1].strip().split(" ")
    processes = []
    for idx, sect in enumerate(sections):
        if idx == 0:
            continue
        process = []
        seed_data = sect.split(":")[1].strip().split("\n")
        for item in seed_data:
            seed_strings = item.strip().split(" ")
            process.append([int(s) for s in seed_strings])
        processes.append(process)

    return seeds, processes


def run(data):

    # Determines if the numbers on the right appear in the winning number list on the left
    # Scores based on a power of two depending on how many matches there are.

    seeds, processes = parseInput(data)
    seeds = set([int(s) for s in seeds])
    result = []
    for seed in seeds:
        for step in processes:
            for process in step:
                diff = process[0] - process[1]
                if process[1] <= seed <= (process[1] + process[2] - 1):
                    seed = seed + diff
                    break
        result.append(seed)
        print(result)

    return min(result)


def run_p2(data):
    '''
        Same as above, but crazy rules involving...more scratch cards?
        Takes a LONG time to run, so use with caution. Probably could
        speed up greatly with some tricks in mapping, but I have my
        answer and need to catch up so will save for later.
    '''
    seeds, processes = parseInput(data)
    seeds = [int(s) for s in seeds]

    # Pair the seed values up...
    min_loc = 999999999
    for seed_group in zip(seeds[::2], seeds[1::2]):
        print(seed_group)
        start_seed = seed_group[0]
        range_length = seed_group[1]
        for i in range(start_seed, range_length + start_seed - 1):
            r = i
            for step in processes:
                for process in step:
                    diff = process[0] - process[1]
                    if process[1] <= r <= (process[1] + process[2] - 1):
                        r = r + diff
                        break
            min_loc = min(min_loc, r)

    return min_loc
