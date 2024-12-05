from ..day04.main import (
    find_cross_pattern,
    find_word,
    turn_grid,
    reverse_grid,
    turn_grid_diagonally,
    get_3x3_chunks,
)


def test_find_word():
    data = ["ABCMASDEF"]
    res = find_word(data, "MAS")
    assert res == 1


def test_find_reversed_word():
    data = ["ABCAASAMF"]
    res = find_word(data, "MAS")
    assert res == 1


def test_find_words_over_lines():
    data = ["SAMUDOAMASAAAW", "MMMMASAASSAAA"]
    res = find_word(data, "MAS")
    assert res == 3


def test_turn_grid():
    data = ["ABCDE", "ABCDE", "ABCDE", "ABCDE", "ABCDE"]
    rotated = ["AAAAA", "BBBBB", "CCCCC", "DDDDD", "EEEEE"]
    res = turn_grid(data)
    assert res == rotated


def test_reverse_grid():
    data = ["ABCDE", "ABCDE", "ABCDE", "ABCDE", "ABCDE"]
    reversed = ["EDCBA", "EDCBA", "EDCBA", "EDCBA", "EDCBA"]
    res = reverse_grid(data)
    assert res == reversed


def test_turn_grid_diagonally():
    data = ["ABCDE", "ABCDE", "ABCDE", "ABCDE", "ABCDE"]
    diag = ["A", "AB", "ABC", "ABCD", "ABCDE", "BCDE", "CDE", "DE", "E"]
    res = turn_grid_diagonally(data)
    assert res == diag


def test_turn_grid_opposite_diagonally():
    data = ["ABCDE", "ABCDE", "ABCDE", "ABCDE", "VWXYZ"]
    diag = ["V", "AW", "ABX", "ABCY", "ABCDZ", "BCDE", "CDE", "DE", "E"]
    res = turn_grid_diagonally(data, -1)
    assert res == diag


def test_get_3x3_chunks():
    data = ["ABCD", "ABCD", "DEFG", "DEFG"]
    chunks = [
        ["ABC", "ABC", "DEF"],
        ["BCD", "BCD", "EFG"],
        ["ABC", "DEF", "DEF"],
        ["BCD", "EFG", "EFG"],
    ]

    res = get_3x3_chunks(data)
    assert res == chunks
