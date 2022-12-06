from day6_task1 import find_marker

stream1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
stream2 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

def test_find_marker():
    assert find_marker(stream1, 4) == 7
    assert find_marker(stream2, 14) == 19