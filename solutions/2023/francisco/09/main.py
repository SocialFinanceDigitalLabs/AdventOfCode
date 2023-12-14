from util import FileParser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def all_zeros(items: list):
    return all(i == 0 for i in items)


def get_extrapolated_p1(sequences: list[list[int]]):
    val = 0
    for history in reversed(sequences):
        val += history[-1] - history[-2]
    return history[-1] + val


def get_extrapolated_p2(sequences: list[list[int]]):
    val = 0
    for history in reversed(sequences):
        val = history[0] - val
        print(val)
    return val


def solve(file, part: int):
    parser = FileParser(dir_path, file)
    data = parser.read()
    histories = [list(map(int, h.split(" "))) for h in data]
    total = 0
    for history in histories:
        sequences = [history]
        while True:
            sequence = sequences[-1]
            diffs = [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]
            sequences.append(diffs)
            if all_zeros(diffs):
                if part == 1:
                    total += get_extrapolated_p1(sequences)
                else:
                    total += get_extrapolated_p2(sequences)

                break
    return total


def part_1(file: str):
    """should return the solution"""
    return solve(file, 1)


def part_2(file):
    """should return the solution"""
    return solve(file, 2)
