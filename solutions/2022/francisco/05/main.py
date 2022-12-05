from util import FileParser
import os
import re


dir_path = os.path.dirname(os.path.realpath(__file__))


def clean_data(data: list):
    stack_count = int((len(data[1]) - 3) / 4) + 1
    middle = data.index("")
    stacks = data[:middle]
    instructions = data[middle + 1 :]
    clean_stacks = []
    for row in stacks[:-1]:
        idx = 0
        clean_row = []
        for s in range(stack_count):
            cell = row[idx : idx + 3].strip("[] ")
            clean_row.append(cell.strip("[] ") if cell else None)
            idx += 3 + 1
        clean_stacks.append(clean_row)

    clean_instructions = []
    for row in instructions:
        numbers = re.findall(r"\d+", row)
        clean_instructions.append(
            {
                "quantity": int(numbers[0]),
                "from": int(numbers[1]) - 1,
                "to": int(numbers[2]) - 1,
            }
        )
    return stack_count, clean_stacks, clean_instructions


def mount_result(stacks: list) -> str:
    result = []
    for stack_idx in range(len(stacks[0])):
        for row in stacks:
            if len(result) == stack_idx + 1:
                continue
            if res := row[stack_idx]:
                result.append(res)
    return "".join(result)


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    stack_count, stacks, instructions = clean_data(data)
    for inst in instructions:
        for _ in range(inst["quantity"]):
            from_row = None
            to_row = None
            for row_idx in range(len(stacks)):
                if from_row is None and stacks[row_idx][inst["from"]] is not None:
                    from_row = row_idx
                if stacks[row_idx][inst["to"]] is None:
                    to_row = row_idx

            if to_row is None:
                stacks.insert(0, [None] * stack_count)
                to_row = 0
                from_row += 1
            stacks[to_row][inst["to"]] = stacks[from_row][inst["from"]]
            stacks[from_row][inst["from"]] = None

    return mount_result(stacks)


def clean_data_2(data: list):
    middle = data.index("")
    _stacks = data[: middle - 1]
    stack_count = int(data[middle - 1].split()[-1])
    stacks = [[] for _ in range(stack_count)]
    for row in _stacks:
        idx = 0
        for s_idx in range(stack_count):
            cell = row[idx : idx + 3].strip("[] ") or None
            stacks[s_idx].append(cell)
            idx += 3 + 1

    stacks = [list(reversed(s)) for s in stacks]
    _instructions = data[middle + 1 :]

    instructions = []
    for row in _instructions:
        numbers = re.findall(r"\d+", row)
        instructions.append(
            {
                "quantity": int(numbers[0]),
                "from": int(numbers[1]) - 1,
                "to": int(numbers[2]) - 1,
            }
        )
    return stacks, instructions


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    stacks, instructions = clean_data_2(data)
    for inst in instructions:
        from_range = []
        to_range = []
        for idx, cell in enumerate(reversed(stacks[inst["from"]])):
            if len(from_range) == inst["quantity"]:
                break
            if cell is not None:
                from_range.append(len(stacks[inst["from"]]) - idx - 1)

        for idx, cell in enumerate(stacks[inst["to"]]):
            if len(to_range) == inst["quantity"]:
                break
            if cell is None:
                to_range.append(idx)
        
        from_range = list(reversed(from_range))

        from_cells = stacks[inst["from"]][from_range[0] : from_range[-1] + 1]
        if not to_range:
            stacks[inst["to"]].extend(from_cells)
        else:
            stacks[inst["to"]][to_range[0] : to_range[-1] + 1] = from_cells
        stacks[inst["from"]][from_range[0] : from_range[-1] + 1] = [None] * len(
            from_range
        )

    result = []
    for stack in stacks:
        result.append([c for c in stack if c is not None][-1])
    return "".join(result)
