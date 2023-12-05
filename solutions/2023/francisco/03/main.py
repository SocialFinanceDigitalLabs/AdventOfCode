from util import FileParser
import os
from dataclasses import dataclass

dir_path = os.path.dirname(os.path.realpath(__file__))


def validate_cell(row: str, cell_i: int) -> bool:
    """returns True if next to character. False if inconclusive"""
    try:
        cell = row[cell_i]
        if cell != "." and not cell.isdigit():
            return True
    except IndexError:
        return False
    return False


def validate_row(row: str, start_number_i: int, end_number_i: int) -> bool:
    results = []
    results.append(validate_cell(row, start_number_i - 1))
    for sub_nr_i in range(start_number_i, end_number_i + 2):
        results.append(validate_cell(row, sub_nr_i))
    return any(results)


def log_row(row: str, start: int, end: int):
    if start > 0:
        start = start - 1
    if end + 1 < len(row):
        end = end + 1
    print(row[start : end + 1])


def log_neighbourhood(data: list[str], start: int, end: int, row_id: int):
    if row_id > 0:
        log_row(data[row_id - 1], start, end)

    log_row(data[row_id], start, end)

    if row_id + 1 < len(data):
        log_row(data[row_id + 1], start, end)


def is_part_number(
    data: list[str], start_number_i: int, end_number_i: int, row_id: int
) -> bool:
    row = data[row_id]
    results = []

    # cells before and after the number
    results.append(validate_cell(row, start_number_i - 1))
    results.append(validate_cell(row, end_number_i + 1))
    if any(results):
        return True

    # prev row
    if row_id > 0:
        row = data[row_id - 1]
        results.append(validate_row(row, start_number_i, end_number_i))
        if any(results):
            return True

    # next row
    if row_id + 1 < len(data):
        row = data[row_id + 1]
        results.append(validate_row(row, start_number_i, end_number_i))
        if any(results):
            return True
    return any(results)


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    numbers = []
    for row_id, row in enumerate(data):
        number = ""
        for el_id, element in enumerate(row):
            if element.isdigit():
                number = number + element
            if el_id == len(row) - 1 or not element.isdigit():
                # if in last element of the row or
                if number:
                    start_nr_id = el_id - len(number)
                    end_nr_id = el_id - 1
                    result = is_part_number(data, start_nr_id, end_nr_id, row_id)
                    if result:
                        numbers.append(int(number))
                    number = ""
    print(numbers)
    return sum(numbers)


@dataclass
class Number:
    start: int
    end: int
    value: str


def detect_numbers(row: list[str]) -> list[Number]:
    """returns start and end pos of each number found"""
    bounds = []
    number = ""
    for el_id, element in enumerate(row):
        if element.isdigit():
            number = number + element

        if not element.isdigit() and number:
            start = el_id - len(number)
            end = el_id - 1
            bounds.append(Number(start, end, int(number)))
            number = ""
            continue

        if el_id == len(row) - 1 and number:
            start = el_id - len(number) + 1
            end = el_id
            bounds.append(Number(start, end, int(number)))
            break

    return bounds


def is_adjacent(bound: int, el_id: int) -> bool:
    return bound == el_id or bound + 1 == el_id or bound - 1 == el_id


def get_adjacent_numbers(rows: list[str], el_id: int) -> list[Number]:
    """count the numbers adjacent to a gear element"""
    adjacents = []
    for row in rows:
        numbers = detect_numbers(row)
        for number in numbers:
            if is_adjacent(number.start, el_id):
                adjacents.append(number)
            elif is_adjacent(number.end, el_id):
                adjacents.append(number)
    return adjacents


def get_adjacent_rows(data: list[str], row_id: int):
    rows = []
    if row_id > 0:
        rows.append(data[row_id - 1])

    rows.append(data[row_id])
    if row_id + 1 < len(data):
        rows.append(data[row_id + 1])
    return rows


def is_gear(el: str):
    return el == "*"


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    total = 0
    for row_id, row in enumerate(data):
        for el_id, element in enumerate(row):
            if is_gear(element):
                rows = get_adjacent_rows(data, row_id)
                adjacent = get_adjacent_numbers(rows, el_id)
                if len(adjacent) == 2:
                    total += adjacent[0].value * adjacent[1].value

    return total
