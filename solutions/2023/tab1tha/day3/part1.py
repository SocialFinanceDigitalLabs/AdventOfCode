import re


def get_numbers(file: str) -> list:
    pattern = re.compile(r"(\d+)")
    numbers = pattern.findall(file)
    return numbers


def get_num_indices(engine_data_lines: list, num: str) -> tuple:
    for row_num in range(len(engine_data_lines)):
        row = engine_data_lines[row_num]
        if num in row:
            col_num = row.index(num)
            return row_num, col_num
    return None, None


def within_bounds(neighbor_loc: tuple, data_span: tuple) -> bool:
    # can be a general util func
    row_adj, col_adj = neighbor_loc
    row_span, col_span = data_span
    if (row_adj < 0) or (row_adj > row_span):
        return False
    if (col_adj < 0) or (col_adj > col_span):
        return False
    return True


def not_num_loc(neighbor_loc: tuple, num_loc: tuple) -> bool:
    row_adj, col_adj = neighbor_loc
    num_row, num_col = num_loc
    if (row_adj == num_row) and (col_adj == num_col):
        return False
    return True


def get_adjacent_values(engine_data_lines: list, num_loc: tuple, num_len: int) -> list:
    num_row, num_col = num_loc
    # if the number 467 starts at col0, then the last digit is at col2
    final_col = num_col + (num_len - 1)

    # define maximum row and col values
    data_span = (len(engine_data_lines) - 1, len(engine_data_lines[0]) - 1)
    neighbors = []
    while num_col <= final_col:
        # neighbors per digit in num
        for row_adj in range(num_row - 1, num_row + 2):
            for col_adj in range(num_col - 1, num_col + 2):
                neighbor_loc = (row_adj, col_adj)
                if within_bounds(neighbor_loc, data_span) & not_num_loc(
                    neighbor_loc, num_loc
                ):
                    neighbors.append(engine_data_lines[row_adj][col_adj])
        # move to next digit in num
        num_col += 1
    neighbors = sorted(list(set(neighbors)))
    return neighbors


def is_part_number(engine_data_lines, num: str) -> bool:
    num_loc = get_num_indices(engine_data_lines, num)
    neighbors = get_adjacent_values(engine_data_lines, num_loc, len(num))
    could_be_symbol = [
        element for element in neighbors if not element.isdigit() and element != "."
    ]
    if len(could_be_symbol) == 0:
        return False
    elif len(could_be_symbol) > 0:
        return True


def day3_part1(filepath: str) -> int:
    with open(filepath, "r") as f:
        engine_data = f.read()

    numbers = get_numbers(engine_data)
    engine_data_lines = engine_data.split("\n")
    # num_indices = get_num_indices(engine_data_lines, numbers)
    part_numbers = []
    for num in numbers:
        if is_part_number(engine_data_lines, num):
            part_numbers.append(int(num))
    return sum(part_numbers)


if __name__ == "__main__":
    result = day3_part1(filepath="day3\input.txt")
    print(result)
