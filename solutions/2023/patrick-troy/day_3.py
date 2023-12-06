from aocd import get_data

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=3, year=2023, session=session).split("\n")

test = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


symbols = ["*", "#", "+", "-", "$", "@", "=", "%", "/", "&"]


def _get_value(co_ord: tuple, dictionary_list: list):
    for d in dictionary_list:
        if co_ord in d:
            return d[co_ord]


def solve(puzzle_input):
    co_ords = []
    for x, row in enumerate(puzzle_input):
        for y, cell in enumerate(row):
            try:
                cell = {(x, y): int(cell)}
            except:
                cell = {(x, y): cell}
            co_ords.append(cell)

    matching_co_ords = []
    for x in range(len(puzzle_input)):
        for y in range(len(puzzle_input)):
            if (
                    isinstance(_get_value((x, y), co_ords), int) and
                    (_get_value((x+1, y), co_ords) in symbols
                     or _get_value((x-1, y), co_ords) in symbols
                     or _get_value((x, y+1), co_ords) in symbols
                     or _get_value((x, y-1), co_ords) in symbols
                     or _get_value((x+1, y+1), co_ords) in symbols
                     or _get_value((x-1, y-1), co_ords) in symbols
                     or _get_value((x-1, y+1), co_ords) in symbols
                     or _get_value((x+1, y-1), co_ords) in symbols)
            ):

                matching_co_ords.append((x, y))

    overlapping_co_ords = []
    for i in range(len(matching_co_ords)-1):
        if matching_co_ords[i][0] == matching_co_ords[i+1][0]:
            if matching_co_ords[i][1] == matching_co_ords[i+1][1]-1:
                overlapping_co_ords.append(matching_co_ords[i])

    non_overlapping_co_ords = [x for x in matching_co_ords if x not in overlapping_co_ords]

    numbers = []
    for x, y in non_overlapping_co_ords:
        if isinstance(_get_value((x, y-1), co_ords), int):
            if isinstance(_get_value((x, y-2), co_ords), int):
                numbers.append(int(f"{_get_value((x, y-2), co_ords)}{_get_value((x, y-1), co_ords)}{_get_value((x, y), co_ords)}"))
            elif isinstance(_get_value((x, y+1), co_ords), int):
                numbers.append(int(f"{_get_value((x, y - 1), co_ords)}{_get_value((x, y), co_ords)}{_get_value((x, y+1), co_ords)}"))
            else:
                numbers.append(int(f"{_get_value((x, y - 1), co_ords)}{_get_value((x, y), co_ords)}"))

        elif isinstance(_get_value((x, y+1), co_ords), int):
            if isinstance(_get_value((x, y+2), co_ords), int):
                numbers.append(int(f"{_get_value((x, y), co_ords)}{_get_value((x, y + 1), co_ords)}{_get_value((x, y + 2), co_ords)}"))
            elif isinstance(_get_value((x, y-1), co_ords), int):
                numbers.append(int(f"{_get_value((x, y - 1), co_ords)}{_get_value((x, y), co_ords)}{_get_value((x, y + 1), co_ords)}"))
            else:
                numbers.append(int(f"{_get_value((x, y), co_ords)}{_get_value((x, y + 1), co_ords)}"))

        else:
            numbers.append(int(f"{_get_value((x, y), co_ords)}"))

    print(sum(numbers))


assert solve(test) == 4361


