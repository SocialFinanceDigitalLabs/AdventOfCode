from aoc_2022_kws.day_13 import test_order


def test_ordering():

    assert test_order(1, 2) == -1
    assert test_order(2, 1) == 1
    assert test_order(1, 1) == 0

    assert test_order([1, 2], [1, 2]) == 0
    assert test_order([2, 2], [1, 2]) == 1
    assert test_order([1, 2], [2, 2]) == -1

    assert test_order(1, [1, 2, 3]) == -1
    assert test_order(1, [2, 2, 3]) == -1
    assert test_order(2, [1, 2, 3]) == 1

    assert test_order([1, 2, 3], 1) == 1
    assert test_order([2], 1) == 1

    assert test_order([], []) == 0
    assert test_order([[]], []) == 1
    assert test_order([], [[]]) == -1
