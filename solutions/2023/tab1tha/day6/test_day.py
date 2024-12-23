import os

from day6.part1 import day6_part1, error_margin, hold_options, read_stats
from day6.part2 import compute_win_bound, day6_part2, large_hold_options, read_stat


def test_read_stats():
    test_data = """Time:      7  15   30
    Distance:  9  40  200
    """
    assert read_stats(test_data) == [("7", "9"), ("15", "40"), ("30", "200")]


def test_hold_options():
    assert hold_options(time=7, distance=9) == [2, 3, 4, 5]

    race2_options = hold_options(time=15, distance=40)
    assert race2_options[0] == 4
    assert race2_options[-1] == 11
    assert len(race2_options) == 8

    race3_options = hold_options(time=30, distance=200)
    assert race3_options[0] == 11
    assert race3_options[-1] == 19
    assert len(race3_options) == 9


def test_compute_win_bound():
    assert compute_win_bound(time=7, distance=9, descend=True) == 2
    assert compute_win_bound(time=7, distance=9, descend=False) == 5

    assert compute_win_bound(time=15, distance=40, descend=True) == 4
    assert compute_win_bound(time=15, distance=40, descend=False) == 11

    assert compute_win_bound(time=30, distance=200, descend=True) == 11
    assert compute_win_bound(time=30, distance=200, descend=False) == 19


def test_error_margin():
    assert error_margin([4, 8, 9]) == 288


def test_day6_part1():
    test_data = """Time:      7  15   30
    Distance:  9  40  200
    """
    sample_data = "test_part1.txt"
    with open(sample_data, "w") as f:
        f.write(test_data)
    assert day6_part1(filepath=sample_data) == 288
    os.remove(sample_data)


def test_read_stat():
    test_data = """Time:      7  15   30
    Distance:  9  40  200
    """
    assert read_stat(test_data) == (71530, 940200)


def test_large_hold_options():
    assert large_hold_options(time=7, distance=9) == (2, 5)
    assert large_hold_options(time=15, distance=40) == (4, 11)
    assert large_hold_options(time=30, distance=200) == (11, 19)
    assert large_hold_options(time=71530, distance=940200) == (14, 71516)


def test_day6_part2():
    test_data = """Time:      7  15   30
    Distance:  9  40  200
    """
    sample_data = "test_part2.txt"
    with open(sample_data, "w") as f:
        f.write(test_data)

    assert day6_part2(filepath=sample_data) == 71503
    os.remove(sample_data)
