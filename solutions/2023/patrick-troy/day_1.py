from aocd import get_data

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=1, year=2023, session=session).split("\n")

test = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]


def solve_1(puzle_input: list) -> int:
    integers = []
    for row in puzle_input:
        row_ints = []
        for i in row:
            try:
                i = int(i)
                row_ints.append(i)
            except:
                pass
        integers.append(row_ints)

    strings = []
    for row in integers:
        new_row = str(row[:1][0]) + str(row[-1:][0])
        new_row = int(new_row)
        strings.append(new_row)

    total = sum(strings)
    return total


assert solve_1(test) == 142

print(solve_1(data))

test_2 = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]

num_to_int = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def convert_num_to_int(puzzle_input: list, converter: dict) -> list:
    integers = []
    for row in puzzle_input:
        for value in converter:
            if value in row:
                row = row.replace(value, f"{value}{converter[value]}{value}")
        integers.append(row)
    return integers


assert solve_1(convert_num_to_int(test_2, num_to_int)) == 281

print(solve_1(convert_num_to_int(data, num_to_int)))
