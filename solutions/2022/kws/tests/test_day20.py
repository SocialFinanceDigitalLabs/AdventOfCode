import pytest
from aoc_2022_kws.config import config
from aoc_2022_kws.day_20 import Entry, from_extended_index, input_to_list


@pytest.fixture
def sample_file():
    return (config.SAMPLE_DIR / "day20.txt").read_text()


def test_shuffle():
    my_test = list(range(10))

    assert from_extended_index(my_test, 5) == 5
    assert from_extended_index(my_test, 15) == 5
    assert from_extended_index(my_test, 25) == 5
    assert from_extended_index(my_test, 1001) == 1

    assert from_extended_index(my_test, -5) == 5
    assert from_extended_index(my_test, -15) == 5
    assert from_extended_index(my_test, -1001) == 9


def test_input_to_list(sample_file):
    input_data = input_to_list(sample_file)
    assert input_data[0] == Entry(1, 0)
