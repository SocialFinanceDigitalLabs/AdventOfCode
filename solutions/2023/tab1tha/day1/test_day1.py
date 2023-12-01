from part1 import calib_sum, day1_part1, get_calibration_values
from part2 import day2_part2, words_and_nums


def test_get_calibration_values():
    assert get_calibration_values("1abc2") == 12
    assert get_calibration_values("pqr3stu8vwx") == 38
    assert get_calibration_values("a1b2c3d4e5f") == 15
    assert get_calibration_values("treb7uchet") == 77


def test_calib_sum():
    assert calib_sum([12, 38, 15, 77]) == 142
    assert calib_sum([29, 83, 13, 24, 42, 14, 76]) == 281


def test_words_and_nums():
    assert words_and_nums("two1nine") == 29
    assert words_and_nums("eightwothree") == 83
    assert words_and_nums("abcone2threexyz") == 13
    assert words_and_nums("xtwone3four") == 24
    assert words_and_nums("4nineeightseven2") == 42
    assert words_and_nums("zoneight234") == 14
    assert words_and_nums("7pqrstsixteen") == 76


def test_day1_part1():
    test_data = """1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet"""

    with open("test_day1.txt", "w") as f:
        f.write(test_data)

    assert day1_part1(filepath="test_day1.txt") == 142


def test_day1_part2():
    test_data = """two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen"""

    with open("test_day2.txt", "w") as f:
        f.write(test_data)

    assert day2_part2(filepath="test_day2.txt") == 281
