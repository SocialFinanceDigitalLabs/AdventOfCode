import re

from part1 import hold_options


def read_stat(data: str) -> list:
    lines = data.splitlines()
    times = re.compile(r"(\d+)").findall(lines[0])
    distances = re.compile(r"(\d+)").findall(lines[1])
    time = int("".join(times))
    distance = int("".join(distances))
    return time, distance


def day6_part2(filepath: str):
    with open(filepath, "r") as f:
        data = f.read()
    time, distance = read_stat(data)
    options = hold_options(time, distance)
    return len(options)


if __name__ == "__main__":
    result = day6_part2(filepath="day2\input.txt")
    print(result)
