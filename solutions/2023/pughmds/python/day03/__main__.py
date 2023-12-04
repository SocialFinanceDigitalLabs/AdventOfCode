import math

EXPECTED_TEST_ANSWER_PART1 = [4361]
EXPECTED_TEST_ANSWER_PART2 = [467835]


def find_non_numerical_indices(array, type=None):
    """
    A.I. Simplified version of logic...though I don't find it as easy to read...
    We want to find the locations of any symbol that isn't
    a number, or a dot (.), and return the coordinates of that position
    """
    return [
        (i, j)
        for i, row in enumerate(array)
        for j, element in enumerate(row)
        if type is None
        and not (element.isnumeric() or element in [".", " ", "\n"])
        or type is not None
        and element == type
    ]


"""
Original version of above code
def find_non_numerical_indices(array, type=None):
    '''
    We want to find the locations of any symbol that isn't
    a number, or a dot (.), and return the coordinates of that position
    '''
    non_numerical_indices = []

    # Loop over string one at a time, trying to find needed character
    for i, row in enumerate(array):
        for j, element in enumerate(row):
            if type is None:
                # For part 1, we were looking for any symbol
                if not (element.isnumeric() or element in [".", " ", "\n"]):
                    non_numerical_indices.append((i, j))
            else:
                # For part 2, we were looking only for a specified type (the *)
                if element == type:
                    non_numerical_indices.append((i, j))

    return non_numerical_indices
"""

def find_numerical_indices(array):
    """
    This function looks for any numbers in an array of strings,
    locates their starting coordinates, and ending coordinates
    effectively giving enough points to define a straight line.
    """
    numbers_with_indices = []
    for i, row in enumerate(array):
        start_index = None
        for j, char in enumerate(row):
            # Loop through whole grid
            if char.isdigit():
                # Found a digit! If this is the first, it is a start index
                if start_index is None:
                    start_index = j
            elif start_index is not None:
                # If we already found a start digit, we're looking for it to end
                # The first non-digit symbol will indicate we no longer have a number
                end_index = j - 1
                # Convert to integer for later calculations
                number = int(row[start_index : end_index + 1])
                numbers_with_indices.append(((i, start_index), (i, end_index), number))
                start_index = None

        # Check for a number at the end of the row
        if start_index is not None:
            end_index = len(row) - 1
            number = int(row[start_index : end_index + 1])
            numbers_with_indices.append(((i, start_index), (i, end_index), number))

    return numbers_with_indices


def is_adjacent(point1, point2, target_point):
    """
    Since each number is defined as a line, we can just use a distance-like
    formula to look for any point that is within one space from that line
    """
    x0, y0 = point1  # starting point of number
    x1, y1 = point2  # ending point of number
    xt, yt = target_point  # The "gear" or * character

    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            # Loop over the points in the number and get distance between number and gear
            dx = abs(xt - x)
            dy = abs(yt - y)

            if dx <= 1 and dy <= 1:
                # If the gear is one off of the line, it's adjacent!
                return True
    # no numbers found near gear
    return False


def get_numbers_with_indices(symbols, numbers):
    """
    Once we found all of the numbers, and all of the symbols,
    we can loop over them to check if they're adjacent to each other.
    If they're adjacent, then we can add them to the list.
    """
    found_numbers = []
    for start, end, number in numbers:
        for symbol in symbols:
            result = is_adjacent(start, end, symbol)
            if result:
                found_numbers.append(number)
                break

    return found_numbers


def get_numbers_adjacent_gears(gears, numbers):
    """
    We need to determine if TWO numbers are next to a "*" symbol.
    If so, it's a gear and we need to store the numbers, ready for
    calculating the ratio.
    """
    ratios = []
    temp_num = 0
    for gear in gears:
        count = 0
        for number in numbers:
            if is_adjacent(number[0], number[1], gear):
                # This point is adjacent
                count += 1
                if count == 1:
                    # We'll want to store this for later if it's the first one found
                    temp_num = number[2]

            if count >= 2:
                # If this is the second one found, then we've found a pair and can store them
                ratios.append(temp_num)
                ratios.append(number[2])
                count = 0
    return ratios


def calculate_ratios(number_list):
    """
    This multiplies each pair of numbers in a list and adds them
    e.g. [1,2,3,4] = 1*2 + 3*4 = 14
    """
    return sum(
        number_list[i] * number_list[i + 1] for i in range(0, len(number_list), 2)
    )


def run(data):
    """
    Gets a grid of numbers, symbols, and dots,
    finds the non-isolated numbers, and adds them up
    """

    # Get location of symbols
    symbol_indices = find_non_numerical_indices(data)
    number_indices = find_numerical_indices(data)
    found = get_numbers_with_indices(symbol_indices, number_indices)

    print("Indices of non-numerical characters:", symbol_indices)
    print("Indices of numerical characters:", number_indices)
    return sum(found)


def run_p2(data):
    """
    Takes a list of values in "data" and determines
    the minimum values of each colour needed for each game
    """
    symbol_indices = find_non_numerical_indices(data, "*")
    number_indices = find_numerical_indices(data)
    found = get_numbers_adjacent_gears(symbol_indices, number_indices)
    result = calculate_ratios(found)

    return result
