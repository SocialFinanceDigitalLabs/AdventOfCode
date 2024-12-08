from ..day02.main import (
    determine_distance_safeness_with_tolerance,
    determine_distance_safeness,
    determine_order_safeness,
    determine_order_safeness_with_tolerance,
    parse_row,
)


def test_determine_distance_safeness_with_tolerance():
    data = [1, 2, 3, 4, 9]
    res = determine_distance_safeness_with_tolerance(data)
    assert res == 1


def test_determine_distance_safeness_with_tolerance():
    data = [18, 12, 10, 9, 7, 6, 6, 7]
    res = determine_distance_safeness_with_tolerance(data)
    assert res == 10


def test_determine_distance_safeness_with_tolerance_out_of_order():
    data = [5, 4, 6, 7, 8, 9]
    res = determine_distance_safeness_with_tolerance(data)
    assert res == 1


def test_determine_distance_safeness_with_tolerance_descend_after_repeat():
    data = [17, 17, 15, 12, 11, 9, 7, 5]
    res = determine_distance_safeness_with_tolerance(data)
    assert res == 1


def test_determine_distance_safeness_with_tolerance_extra_number():
    data = [1, 2, 3, 4, 9, 10]
    res = determine_distance_safeness_with_tolerance(data)
    assert res == 2


def test_determine_distance_incorrectness_with_tolerance():
    data = [1, 6, 7, 8, 15, 16]
    res = determine_distance_safeness_with_tolerance(data)
    assert res == 5


def test_determine_distance_safeness():
    data = [1, 2, 3, 4, 7]
    res = determine_distance_safeness(data)
    assert res == True


def test_determine_distance_unsafeness():
    data = [1, 2, 8, 9, 10]
    res = determine_distance_safeness(data)
    assert res == False


def test_determine_distance_sameness():
    data = [1, 2, 2, 3, 4, 5, 7]
    res = determine_distance_safeness(data)
    assert res == False


def test_determine_order_safeness():
    data = [1, 4, 6, 8, 9, 12]
    res = determine_order_safeness(data)
    assert res == True


def test_determine_order_safeness_descending():
    data = [12, 9, 8, 6, 4, 1]
    res = determine_order_safeness(data)
    assert res == True


def test_determine_order_unsafeness():
    data = [1, 4, 6, 9, 8, 12]
    res = determine_order_safeness(data)
    assert res == False


def test_determine_order_safeness_with_tolerance():
    data = [1, 2, 3, 5, 6, 7, 10]
    res = determine_order_safeness_with_tolerance(data)
    assert res == 0


def test_determine_order_safeness_with_tolerance_of_one():
    data = [1, 2, 3, 6, 5, 7, 10]
    res = determine_order_safeness_with_tolerance(data)
    assert res == 1


def test_determine_order_safeness_with_tolerance_descending():
    data = [11, 9, 6, 4, 2, 1]
    res = determine_order_safeness_with_tolerance(data)
    assert res == 0


def determine_order_unsafeness_with_tolerance():
    data = [2, 1, 3, 6, 5, 7, 10]
    res = determine_order_safeness_with_tolerance(data)
    assert res == 2


def test_parse_row():
    input = "4 15 36 21 1 9"
    res = parse_row(input)
    assert res == [4, 15, 36, 21, 1, 9]
