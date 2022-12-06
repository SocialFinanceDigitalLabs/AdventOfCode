from aocd import get_data

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

cleaning_assignments = get_data(day=4, year=2022, session=session).split("\n")

pairs = [pair.split(",") for pair in cleaning_assignments]

# PART 1
def _calculate_difference(range_string: str):
    values = range_string.split("-")
    min_value = int(values[0])
    max_value = int(values[1])
    difference = max_value - min_value
    return difference


def find_biggest_difference(range_string_1: str, range_string_2: str):
    """
    Calculate the biggest range difference between two strings representing ranges separated with a hyphen

    :param range_string_1: string of two numbers with hyphen in between representing range
    :param range_string_2: string of two numbers with hyphen in between representing range
    return 0 if range_string_1 range is greater than range_string_2 otherwise return 1
    """
    return 0 if _calculate_difference(range_string_1) > _calculate_difference(range_string_2) else 1


def split_assignments(assignments: str):
    assignment = assignments.split("-")
    return assignment


total = 0

for pair in pairs:
    if find_biggest_difference(pair[0], pair[1]) == 1:
        if int(split_assignments(pair[0])[0]) >= int(split_assignments(pair[1])[0]) \
                and int(split_assignments(pair[0])[1]) <= int(split_assignments(pair[1])[1]):
            total += 1
    else:
        if int(split_assignments(pair[1])[0]) >= int(split_assignments(pair[0])[0]) \
                and int(split_assignments(pair[1])[1]) <= int(split_assignments(pair[0])[1]):
            total += 1

print(total)

# PART 2
def range_to_list(range_string: str):
    lower_range = int(split_assignments(range_string)[0])
    upper_range = int(split_assignments(range_string)[1])
    range_list = list(range(lower_range, upper_range+1))
    return range_list


total = 0

for pair in pairs:
    if any(x in range_to_list(pair[1]) for x in range_to_list(pair[0])):
        total += 1

print(total)
