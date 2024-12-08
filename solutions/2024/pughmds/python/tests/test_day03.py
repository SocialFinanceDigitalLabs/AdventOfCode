from ..day03.main import get_operations, parse_mul, strip_out_missed_code


def test_get_operations():
    test_input = "ab 2346cmul(2,4)defg 0-1897y5"
    matches = get_operations(test_input)

    assert matches == ["mul(2,4)"]


def test_multiple_get_operations():
    test_input = "ab 2346cmul(2,4)defg 0-18 mul(1,1)97y5jasfasd'#'l;asdfgh asdfmul(9,2)l;aksedyut89o32"
    matches = get_operations(test_input)

    assert matches == ["mul(2,4)", "mul(1,1)", "mul(9,2)"]


def test_parse_mul():
    test_string = "mul(2,3)"
    assert 6 == parse_mul(test_string)

    test_string = "mul(23,11)"
    assert 253 == parse_mul(test_string)


def test_strip_out_missed_code():
    test_string = "mul(2,3)don't()mul(2,2)do()mul(1,1)"
    result = strip_out_missed_code(test_string)
    assert result == "mul(2,3)mul(1,1)"


def test_strip_out_missed_code_with_trailing_dont():
    test_string = "mul(2,3)don't()mul(2,2)do()mul(1,1)mul(3,4)don't()mul(5,4)"
    result = strip_out_missed_code(test_string)
    assert result == "mul(2,3)mul(1,1)mul(3,4)"
