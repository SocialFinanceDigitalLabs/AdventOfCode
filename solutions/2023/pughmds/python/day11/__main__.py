import math

EXPECTED_TEST_ANSWER_PART1 = [374, 22, 6]
EXPECTED_TEST_ANSWER_PART2 = [1030, 102, 6]

class Galaxy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_distance(g1, g2):
    distance = abs(g2.x - g1.x) + abs(g2.y - g1.y)
    return distance

def get_empty(map):
    empty_rows = []

    for y_idx, line in enumerate(map):
        if "#" not in line:
            empty_rows.append(y_idx)
    return empty_rows

def duplicate_row(lst, index):

    row_to_dup = lst[index]
    lst.insert(index, row_to_dup)

    return lst


def duplicate_col(lst, index):
    if not lst:
        return

    if 0 <= index < len(lst[0]):
        for i in range(len(lst)):
            # Insert a duplicate of the character at the specified index
            lst[i] = lst[i][:index] + lst[i][index] + lst[i][index:]
    else:
        print("Index out of range")
    return lst

def find_galaxies(data):
    galaxies = []
    for y_idx, line in enumerate(data):
        indices = []
        start_index = 0
        try:
            while True:
                index = line.index("#", start_index)
                indices.append(index)
                start_index = index + 1
        except ValueError:
            pass

        for index in indices:
            galaxies.append(Galaxy(index, y_idx))
    return galaxies

def get_distance_sum(galaxies):
    total = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            galaxy = galaxies[i]
            pair_galaxy = galaxies[j]
            distance = get_distance(galaxy, pair_galaxy)
            if distance > 0:
                total += distance
    return total


def get_distance_sum_expanded(galaxies, empty_rows, empty_cols, distance_factor):
    total = 0
    distance_factor -= 1
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            distance = get_distance(galaxies[i], galaxies[j])
            # First, work out if we crossed any row boundaries (Y)
            if galaxies[i].y > galaxies[j].y:
                first_val = galaxies[j].y
                second_val = galaxies[i].y
            else:
                first_val = galaxies[i].y
                second_val = galaxies[j].y

            # Work out how many times we need to expand on the distance
            crossed_boundaries = [x for x in empty_rows if first_val <= x < second_val]
            if len(crossed_boundaries) > 0:
                distance += (len(crossed_boundaries) * distance_factor)

            # Next, work out if we crossed any column boundaries (X)
            if galaxies[i].x > galaxies[j].x:
                first_val = galaxies[j].x
                second_val = galaxies[i].x
            else:
                first_val = galaxies[i].x
                second_val = galaxies[j].x

            crossed_boundaries = [x for x in empty_cols if first_val <= x < second_val]
            if len(crossed_boundaries) > 0:
                distance += (len(crossed_boundaries) * distance_factor)

            total += distance
    return total

def run(data):
    """
    Actually physically modify the map to have the needed values.
    """
    # Find a list of empty rows
    empty_rows = get_empty(data)
    if len(empty_rows) > 0:
        empty_rows.sort(reverse=True)

    # find a list of empty columns
    empty_cols = get_empty(list(map(list, zip(*data))))
    if len(empty_cols) > 0:
        empty_cols.sort(reverse=True)

    # Duplicate any rows and columns that are needed
    for row in empty_rows:
        data = duplicate_row(data, row)

    for col in empty_cols:
        data = duplicate_col(data, col)

    # Find all the galaxies
    galaxies = find_galaxies(data)

    # Get the sum of the distances
    total = get_distance_sum(galaxies)
    return total


def run_p2(data):
    """
    To do this, we can't modify the map, but we CAN modify the coordinates
    to create the same effect.
    """
    # First, find all the galaxies
    galaxies = find_galaxies(data)

    # Find a list of empty rows
    empty_rows = get_empty(data)
    if len(empty_rows) > 0:
        empty_rows.sort(reverse=True)

    # find a list of empty columns
    empty_cols = get_empty(list(map(list, zip(*data))))
    if len(empty_cols) > 0:
        empty_cols.sort(reverse=True)

    # Now that we have a list of galaxies, let's find the empty rows and cols
    for row in empty_rows:
        data = duplicate_row(data, row)

    for col in empty_cols:
        data = duplicate_col(data, col)

    # Finally, let's work out the distance sum
    total = get_distance_sum_expanded(galaxies, empty_rows, empty_cols, 1000000)
    return total
