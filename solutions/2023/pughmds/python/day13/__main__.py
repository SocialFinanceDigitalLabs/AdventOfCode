from collections import Counter

EXPECTED_TEST_ANSWER_PART1 = [405, 900, 400, 500]
EXPECTED_TEST_ANSWER_PART2 = [400, 400, 6, 11]


def find_symmetry_line(data):
    """
    UNUSED

    Finds repeated elements in a list of strings. Worked as an initial
    experiment, but found it might be too cumbersome in the long run.
    Have left for reference, but didn't use in the final solution...
    """
    counter = Counter(data)
    duplicates_with_indices = {}

    for idx, item in enumerate(data):
        if counter[item] > 1:
            if item not in duplicates_with_indices:
                duplicates_with_indices[item] = [idx]
            else:
                duplicates_with_indices[item].append(idx)

    return duplicates_with_indices


def split_shapes(data):
    """
    UNUSED

    First I visually split the input into groups of 2D string arrays
    But found that this would be limiting in the long run. Have left for
    reference, but didn't use in the final solution...
    """
    result = []
    current_subarray = []

    for element in data:
        element = element.strip()
        if element:  # Check if the element is non-empty
            current_subarray.append(element)
        elif current_subarray:  # Check if the current subarray is not empty
            result.append(current_subarray)
            current_subarray = []

    if current_subarray:
        result.append(current_subarray)

    return result


def convert_shape_to_binary(shape):
    """
    Converts each line of a shape into a binary representation
    so it makes this problem simply dealing with symmetry in
    a list of numbers instead of a 2D string.
    """
    bin_shape = []
    for row in shape:
        row = row.strip().replace(".", "0").replace("#", "1")
        bin_shape.append(int(row, 2))

    return bin_shape


def find_repeating_indices(lst, smudge=False):
    """
    Find where there are two elements of the list that are the same.
    It may (or may not) be a mirror line!
    """
    repeating_indices = []

    for i in range(1, len(lst)):
        num1 = lst[i]
        num2 = lst[i - 1]
        if num1 == num2:
            repeating_indices.append((i - 1, i))
        elif smudge:
            # Let's also check if numbers are one-off their neighbours?
            comparison_result = check_binary_similarity(num1, num2)
            if comparison_result:
                repeating_indices.append((i - 1, i))
    return repeating_indices


def check_binary_similarity(x, y):
    """
    This function compares (bitwise) two numbers
    and checks to see if they are one bit-flip off
    of each other. If they are, then return true
    as this could be a smudge.
    """
    result = x ^ y
    if bin(result).count("1") == 1:
        return True
    return False


def check_symmetry(shape, index, smudge=False):
    """
    Check to see if a list is symmetrical around the given index
    """

    # First, split the list around the symmetry
    a = shape[: index[1]]
    b = shape[index[1] :]

    # Find the shorter pattern, and match the longer one
    min_length = min(len(a), len(b))
    a = a[-min_length:]
    b = b[:min_length]

    if a == b[::-1] and not smudge:
        # Already a mirror, no need to do anything further
        return len(shape[: index[1]])
    elif smudge:
        # Find the differences between the two lists
        diff = list(set(a) ^ set(b[::-1]))
        if len(diff) == 2:
            # We're only going to act if there's a matching pair
            comparison_result = check_binary_similarity(diff[0], diff[1])
            if comparison_result:
                return len(shape[: index[1]])
            else:
                return -1
        else:
            return -1
    return -1


def count_score(repeats, multiplier, bin_shape, smudge=False):
    """
    Totals up the score to feed to AoC. 100* horiz, 1* vertical
    """
    total = 0
    for index in repeats:
        result = check_symmetry(bin_shape, index, smudge)
        if result > 0:
            total += result * multiplier
    return total


def handle_shape(shape, multiplier, smudge=False):
    """
    Steps to determine and count LOS for a shape
    """
    bin_shape1 = convert_shape_to_binary(shape)
    repeats = find_repeating_indices(bin_shape1, smudge)
    return count_score(repeats, multiplier, bin_shape1, smudge)


def run(data):
    """
    Lines of symmetry
    """
    # First, we need to find any row or column that has a neighbour that matches.
    shapes = split_shapes(data)
    total = 0
    for shape in shapes:
        # The original shape
        total += handle_shape(shape, 100)
        total += handle_shape(["".join(chars) for chars in zip(*shape)], 1)
    return total


def run_p2(data):
    """
    Now we have smudges to worry about...
    """
    shapes = split_shapes(data)
    total = 0
    for shape in shapes:
        # The original shape
        total += handle_shape(shape, 100, True)
        total += handle_shape(["".join(chars) for chars in zip(*shape)], 1, True)
    return total
