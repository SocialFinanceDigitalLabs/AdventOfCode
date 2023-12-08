import re
from functools import reduce


def read_stats(data: str) -> list:
    lines = data.splitlines()
    times = re.compile(r"(\d+)").findall(lines[0])
    distances = re.compile(r"(\d+)").findall(lines[1])
    return list(zip(times, distances))


def hold_options(time: int, distance: int) -> list:
    return [hold for hold in range(time) if (hold * (time - hold) > distance)]


def error_margin(num_options: list) -> int:
    return reduce(lambda x, y: x * y, num_options)


def day6_part1(filepath: str) -> int:
    with open(filepath, "r") as f:
        data = f.read()
    stats = read_stats(data)
    num_options = [
        len(hold_options(int(time), int(distance))) for time, distance in stats
    ]
    return error_margin(num_options)


if __name__ == "__main__":
    result = day6_part1(filepath="day6\input.txt")
    print(result)
