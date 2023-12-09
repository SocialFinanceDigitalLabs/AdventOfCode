from aocd import get_data
import numpy as np

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=9, year=2023, session=session).split("\n")


test = [
    "0 3 6 9 12 15",
    "1 3 6 10 15 21",
    "10 13 16 21 30 45",
]


def solve(puzzle_input, reverse=False):
    sums = []
    for row in puzzle_input:
        if reverse:
            row = np.array(list(reversed(row.split())), dtype=np.int64)
        else:
            row = np.array(row.split(), dtype=np.int64)
        next_row = np.diff(row)

        final_digits = row[-1:]

        while not all(x == next_row[0] for x in next_row):
            final_digits = np.append(final_digits, next_row[-1:])
            next_row = np.diff(next_row)

        if all(x == next_row[0] for x in next_row):
            final_digits = np.append(final_digits, next_row[-1:])

        sums.append(sum(final_digits))
    return sum(sums)


assert solve(test) == 114
print(solve(data))

assert solve(test, reverse=True) == 2
print(solve(data, reverse=True))
