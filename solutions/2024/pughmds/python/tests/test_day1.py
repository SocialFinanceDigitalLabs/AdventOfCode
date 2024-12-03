from ..day01.main import parse_line, parse_data, calculate_distances


def test_calculate_distances():
    list1 = [1, 3, 5]
    list2 = [9, 2, 5]

    expected = [8, 1, 0]

    res = calculate_distances(list1, list2)

    assert res == expected


def test_parse_line():
    data = "1     9"
    res = parse_line(data)
    assert res == (1, 9)


def test_parse_data():
    data = ["1      2", "2      5", "9     1"]

    res = parse_data(data)

    assert res == [[1, 2, 9], [2, 5, 1]]
