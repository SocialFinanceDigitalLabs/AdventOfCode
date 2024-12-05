EXPECTED_TEST_ANSWER_PART1 = [18, 3, 4]
EXPECTED_TEST_ANSWER_PART2 = [9, 0, 2]


def find_word(data: list, word: str) -> int:
    """
    This finds the given word and the reversed version of the word in the data and returns
    the number of times the word is found.
    :param data: A list of strings
    :param word: The word we're looking for
    :return: A count of the number of times that word is found.
    """

    return sum(row.count(word) + row.count(word[::-1]) for row in data)


def turn_grid(data: list) -> list:
    """
    This rotates a grid 90 degrees

    ABC                 ADG
    DEF     becomes     BEH
    GHI                 CFI


    :param data: a list of strings
    :return: a rotated list of strings
    """
    rotated_strings = []
    for i in zip(*data[::-1]):
        rotated_strings.append("".join(i))
    return rotated_strings


def reverse_grid(data: list) -> list:
    """
    This flips a 2d list upside down

    ABC                 GHI
    DEF     becomes     DEF
    GHI                 ABC

    :param data: A list of strings
    :return: a flipped list of strings
    """
    return [row[::-1] for row in data]


def turn_grid_diagonally(data: list, dir: int = 1) -> list:
    """
    This rotates a grid 45 degrees so searching can be done
    in the same way as with a normal grid.

    ABC                     A
    CDE     Becomes         CB
    FGH                    FDC
                            GE
                            H

    There are definitely more efficeint ways to do this that
    aren't as visual, but it's kind of nice to see what's
    going on as well.

    :param data: a list of strings
    :param dir: the direction. Can be 1 (turn right 45 degrees) or -1 (turn left 45 degrees)
    :return: a rotated list of strings
    """
    if dir == -1:
        data = data[::-1]
    width = len(data[0])
    height = len(data)

    rotated_data = []

    for i in range(width + height - 1):
        diagonal = []
        for j in range(max(0, i - height + 1), min(i + 1, width)):
            diagonal.append(data[i - j][j])
        rotated_data.append("".join(diagonal))

    return rotated_data


def clean_data(data: list) -> list:
    """
    Removes any extra spaces that sneakily are finding their way into the input
    for some reason...
    :param data: A list of strings
    :return: A list of strings, with any trailing spaces removed
    """
    new_data = []
    for item in data:
        new_data.append(item.strip())
    return new_data


def get_3x3_chunks(data: list) -> list:
    """
    Takes a 2D list of strings and splits
    it into a series of 3x3 chunks to use
    for pattern matching.

    :param data: A list of strings
    :return: a list of lists that represents 3x3 slices of the original data
    """

    chunks = []
    for i in range(len(data) - 2):
        for j in range(len(data[0]) - 2):
            chunk = [row[j : j + 3] for row in data[i : i + 3]]
            chunks.append(chunk)
    return chunks


def find_cross_pattern(grid: list) -> bool:
    """
    Tests for various cross patterns of the three-letter-word
    "MAS".  Could probably make this word-agnostic, but since
    we never needed to...  There are four posible "cross" patterns:

    M M     S S     M S     S M
     A       A       A       A
    S S     M M     M S     S M

    Apparently cross patterns (+) don't count...

    :param grid: The input data which should be a 3x3 grid
    :return: Truth value if there's a pattern match or not
    """
    if grid[1][1] != "A":
        return False
    if (
        grid[0][0] == grid[0][2]
        and grid[2][0] == grid[2][2]
        and grid[0][0] in ["M", "S"]
        and grid[2][0] in ["M", "S"]
        and grid[0][0] != grid[2][0]
    ):
        return True
    if (
        grid[0][0] == grid[2][0]
        and grid[0][2] == grid[2][2]
        and grid[0][0] in ["M", "S"]
        and grid[0][2] in ["M", "S"]
        and grid[0][0] != grid[0][2]
    ):
        return True
    return False


def run(data: list) -> int:
    word_to_find = "XMAS"
    word_count = 0
    data = clean_data(data)
    word_count += find_word(data, word_to_find)
    word_count += find_word(turn_grid(data), word_to_find)
    word_count += find_word(turn_grid_diagonally(data), word_to_find)
    word_count += find_word(turn_grid_diagonally(data, dir=-1), word_to_find)
    return word_count


def run_p2(data: list) -> int:
    x_count = 0
    data = clean_data(data)
    chunks = get_3x3_chunks(data)
    for grid in chunks:
        if find_cross_pattern(grid):
            x_count += 1

    return x_count
