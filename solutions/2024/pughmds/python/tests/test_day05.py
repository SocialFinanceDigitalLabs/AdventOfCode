from ..day05.main import parse_input, check_num, check_update


def test_parse_input():
    data = ["47|53", "97|13", "", "47,53,21", "97,13,15,36,12"]
    res = parse_input(data)
    assert res[0] == {47: [53], 97: [13]}
    assert res[1] == [[47, 53, 21], [97, 13, 15, 36, 12]]


def test_parse_input_multiple():
    data = ["47|53", "97|13", "47|21" "", "47,53,21", "97,13,15,36,12"]
    res = parse_input(data)
    assert res[0] == {47: [53, 21], 97: [13]}
    assert res[1] == [[47, 53, 21], [97, 13, 15, 36, 12]]


def test_check_update_fail():
    rules = {42: [36, 77, 13], 36: [77, 13], 92: [42, 36, 77, 13], 77: [13]}
    data = [42, 13, 36, 77, 92]
    res = check_update(77, data, rules)
    assert res == False


def test_check_update():
    rules = {42: [36, 77, 13], 36: [77, 13], 92: [42, 36, 77, 13], 77: [13]}
    data = [92, 42, 36, 77, 13]
    res = check_update(92, data, rules)
    assert res == True


def test_check_num_move():
    rules = {42: [36, 77, 13], 36: [77, 13], 92: [42, 36, 77, 13], 77: [13]}
    data = [42, 13, 36, 77, 92]
    res = check_num(data, rules, 13)
    assert res == [42, 36, 77, 92, 13]


def test_check_num_move_next():
    rules = {42: [36, 77, 13], 36: [77, 13], 92: [42, 36, 77, 13], 77: [13]}
    data = [42, 36, 92, 77, 13]
    res = check_num(data, rules, 36)
    assert res == [42, 92, 36, 77, 13]


def test_check_num_no_move():
    # We should only move numbers related to the number we're using as a key
    # 13 is out of place, but not based on the current rule...
    rules = {42: [36, 77, 13], 36: [77, 13], 92: [42, 36, 77, 13], 77: [13]}
    data = [42, 92, 36, 13, 77]
    res = check_num(data, rules, 36)
    assert res == [42, 92, 36, 13, 77]
