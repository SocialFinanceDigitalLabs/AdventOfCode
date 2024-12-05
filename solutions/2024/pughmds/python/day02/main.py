EXPECTED_TEST_ANSWER_PART1 = [2]
EXPECTED_TEST_ANSWER_PART2 = [4]


def parse_row(row):
    nums = [int(i) for i in row.strip().split(" ")]
    return nums


def determine_order_safeness(row):
    ordered_row = sorted(row)
    if ordered_row == row or ordered_row == row[::-1]:
        return True
    return False


def determine_order_safeness_with_tolerance(row):
    out_of_order_count_ascending = out_of_order_count_descending = 0
    for i in range(len(row) - 1):
        if row[i] > row[i + 1]:
            out_of_order_count_ascending += 1

    for i in range(len(row) - 1):
        if row[i] < row[i + 1]:
            out_of_order_count_descending += 1

    return min([out_of_order_count_ascending, out_of_order_count_descending])


def determine_distance_safeness(row):
    differences = []
    for i in range(1, len(row)):
        difference = row[i] - row[i - 1]
        differences.append(abs(difference))
    if min(differences) >= 1 and max(differences) <= 3:
        return True
    return False


def determine_duplicates(row):
    duplicates = 0
    if list(set(row)) != row:
        duplicates = abs(len(list(set(row))) - len(row))
    return duplicates


def determine_distance_safeness_with_tolerance(row: list) -> int:
    errors = determine_duplicates(row)

    differences = []
    for i in range(1, len(row)):
        difference = row[i] - row[i - 1]
        differences.append(difference)

    ascending = any(num > 0 for num in row)
    descending = any(num < 0 for num in row)

    if (min(differences) >= 1 and max(differences) <= 3) or (
        min(differences) >= -3 and max(differences) <= -1
    ):
        # All the differences are in the correct range
        return errors

    if any(x > 0 for x in differences) and any(x < 0 for x in differences):
        errors += 1

    for i, num in enumerate(differences):
        if abs(num) > 3:
            if i == len(differences) - 1:
                return errors + 1
            else:
                return errors + (len(differences) - i)

    return sum(1 for num in differences if abs(num) > 3) + errors


def run(data: list) -> int:
    safe_counter = 0
    for row in data:
        row_values = parse_row(row)
        order_res = determine_order_safeness(row_values)
        if order_res:
            dist_res = determine_distance_safeness(row_values)
            if dist_res:
                safe_counter += 1
    return safe_counter


def run_p2(data: list) -> int:
    safe_counter = 0
    for row in data:
        order_res = 0
        dist_res = 0
        row_values = parse_row(row)
        order_res = determine_order_safeness_with_tolerance(row_values)

        if order_res <= 1:
            dup_res = determine_duplicates(row_values)
            dist_res = determine_distance_safeness_with_tolerance(row_values)

            if dist_res + order_res <= 1:
                safe_counter += 1

        if order_res + dist_res > 1:
            print(
                f"Row: {row} has {order_res + dist_res} problems ({order_res} Order, {dup_res} Duplicates, and {dist_res - dup_res} distance)"
            )
        else:
            print(f"OK: {row}")
    return safe_counter
