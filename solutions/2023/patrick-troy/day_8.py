from aocd import get_data
import numpy as np

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=8, year=2023, session=session).split("\n")

test = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]


def _create_dict(puzzle_input):
    puzzle_dict = {"instructions": puzzle_input[0]}
    for row in puzzle_input[2:]:
        puzzle_dict[row.split()[0]] = (row.split()[2][1:4], row.split()[3][0:3])

    return puzzle_dict


def _map_instructions(puzzle_input):
    puzzle_dict = _create_dict(puzzle_input)
    prev_code = "AAA"
    end_code = "ZZZ"
    steps = 0

    while prev_code != end_code:
        for instruction in puzzle_dict["instructions"]:
            if prev_code == end_code:
                break
            elif instruction == "L":
                prev_code = puzzle_dict[prev_code][0]
            elif instruction == "R":
                prev_code = puzzle_dict[prev_code][1]
            steps += 1

    return steps


assert _map_instructions(test) == 6
print(_map_instructions(data))

test_2 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]


def _ghost_instructions(puzzle_input):
    puzzle_dict = _create_dict(puzzle_input)
    starting_nodes = [row for row in puzzle_dict.keys() if row[-1] == "A"]
    all_found = [False for _ in range(len(starting_nodes))]
    steps_until_first_Z = [0 for _ in range(len(starting_nodes))]

    steps = 0
    while not all(all_found):
        for instruction in puzzle_dict["instructions"]:
            if all(all_found):
                break
            if instruction == "L":
                starting_nodes = [puzzle_dict[node][0] for node in starting_nodes]
            elif instruction == "R":
                starting_nodes = [puzzle_dict[node][1] for node in starting_nodes]
            for i, node in enumerate(starting_nodes):
                if node[-1] == 'Z' and steps_until_first_Z[i] == 0:
                    all_found[i] = True

                    steps_until_first_Z[i] = steps + 1
            steps += 1

    steps_until_first_Z = np.array(steps_until_first_Z, dtype=np.int64)
    steps = np.lcm.reduce(steps_until_first_Z)
    return steps


assert _ghost_instructions(test_2) == 6
print(_ghost_instructions(data))
