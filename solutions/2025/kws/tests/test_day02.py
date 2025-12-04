from aoc_2025_kws.day_02 import possible_patterns, is_repeating_pattern


def test_patterns():
    assert possible_patterns("11") == ["1"]
    assert possible_patterns("1122") == ["11", "1"]
    assert possible_patterns("1010") == ["10", "1"]
    assert possible_patterns("1188511885") == ['11885', '1188', "118", '11', '1']



def test_repeating_patterns():
    assert is_repeating_pattern("11") is True
    assert is_repeating_pattern("1122") is False
    assert is_repeating_pattern("1010") is True
    assert is_repeating_pattern("1011") is False
    assert is_repeating_pattern("1188511885") is True
    assert is_repeating_pattern("446446") is True
    assert is_repeating_pattern("10051007") is False

