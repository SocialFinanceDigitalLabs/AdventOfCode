EXPECTED_TEST_ANSWER_PART1 = 2
EXPECTED_TEST_ANSWER_PART2 = 4


def generate_assignment_boundaries(assignment):
    """
    Take each boundary in the assignment and generate a list of values
    to be later be used to compare against other assignments
    """
    boundaries = assignment.split("-")
    boundary_range = range(int(boundaries[0]), int(boundaries[1]) + 1)
    return list(boundary_range)


def subset_in_lists(list1, list2):
    """
    Find which assignments are FULLY contained in other assignments
    """
    if all(item in list1 for item in list2) or all(item in list2 for item in list1):
        return 1
    else:
        return 0


def any_overlap_in_lists(list1, list2):
    """
    Find if an assignment has ANY overlap with any other assignment
    """
    if any(item in list1 for item in list2) or any(item in list2 for item in list1):
        return 1
    else:
        return 0


def run(data):
    match_count = 0
    for row in data:
        elves = row.split(",")
        elf_boundary_pair = []
        for assignment in elves:
            boundary = generate_assignment_boundaries(assignment)
            elf_boundary_pair.append(boundary)

        match_count += subset_in_lists(elf_boundary_pair[0], elf_boundary_pair[1])

    return match_count


def run_p2(data):
    match_count = 0
    for row in data:
        elves = row.split(",")
        elf_boundary_pair = []
        for assignment in elves:
            boundary = generate_assignment_boundaries(assignment)
            elf_boundary_pair.append(boundary)

        match_count += any_overlap_in_lists(elf_boundary_pair[0], elf_boundary_pair[1])

    return match_count
