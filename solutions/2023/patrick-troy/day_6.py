from aocd import get_data
import re
import numpy as np

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=6, year=2023, session=session).split("\n")

test = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]


def _game_dict(puzzle_input):
    for row in puzzle_input:
        if "Time" in row:
            time = re.findall(r"\d+", row)
        elif "Distance" in row:
            distance = re.findall(r"\d+", row)

    game_dict = (dict(zip(time, distance)))
    return game_dict


def _race(time):
    time = int(time)

    distances = []
    for i in range(time):
        distances.append(i*(time-i))
    return distances


def _winning_times(distances, record):
    winning_times = [x for x in distances if x > int(record)]
    return winning_times


def _game_dict_2(puzzle_input):
    for row in puzzle_input:
        row = row.replace(" ", "")
        if "Time" in row:
            time = re.findall(r"\d+", row)
        elif "Distance" in row:
            distance = re.findall(r"\d+", row)

    game_dict = (dict(zip(time, distance)))
    return game_dict


def solve(puzzle_input, game):
    winning_times = []
    game_dict = _game_dict(puzzle_input) if game == "game_1" else _game_dict_2(puzzle_input)
    for time, record in game_dict.items():
        distances = _race(time)
        winning_times.append(len(_winning_times(distances, record)))

    return np.prod(winning_times)


assert solve(test, game="game_1") == 288
print(solve(data, game="game_1"))

assert solve(test, game="game_2") == 71503
print(solve(data, game="game_2"))
