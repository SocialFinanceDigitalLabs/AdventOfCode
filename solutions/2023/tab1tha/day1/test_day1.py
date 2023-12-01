from part1 import get_calibration_values, calib_sum

def test_get_calibration_values():
    assert get_calibration_values("1abc2") == 12
    assert get_calibration_values("pqr3stu8vwx") == 38
    assert get_calibration_values("a1b2c3d4e5f") == 15
    assert get_calibration_values("treb7uchet") == 77

def test_calib_sum():
    assert calib_sum([12,38,15,77]) == 142