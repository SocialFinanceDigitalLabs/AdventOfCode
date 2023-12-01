from part1 import get_calibration_values, calib_sum
from part2 import word_to_num

def test_get_calibration_values():
    assert get_calibration_values("1abc2") == 12
    assert get_calibration_values("pqr3stu8vwx") == 38
    assert get_calibration_values("a1b2c3d4e5f") == 15
    assert get_calibration_values("treb7uchet") == 77

def test_calib_sum():
    assert calib_sum([12,38,15,77]) == 142
    assert calib_sum([29,83,13,24,42,14,76]) == 281

def test_word_to_num():
    assert word_to_num("two1nine") == "219"
    assert word_to_num("eightwothree") == "8wo3"
    assert word_to_num("abcone2threexyz") == "abc123xyz"
    assert word_to_num("xtwone3four") == "x2ne34"
    assert word_to_num("4nineeightseven2") == "49872"
    assert word_to_num("zoneight234") == "z1ight234"
    assert word_to_num("7pqrstsixteen") == "7pqrst6teen"
