import pytest
from aoc_2022_kws.config import config
from aoc_2022_kws.day_24 import Coordinate, Direction, ValleyMap, parse_map


@pytest.fixture
def super_simple_sample_map():
    input_data = (config.SAMPLE_DIR / "day24-simple.txt").read_text()
    return ValleyMap.from_input_data(tuple(parse_map(input_data)))


@pytest.fixture
def simple_sample_map():
    input_data = (config.SAMPLE_DIR / "day24.txt").read_text()
    return ValleyMap.from_input_data(tuple(parse_map(input_data)))


@pytest.fixture
def puzzle_map():
    input_data = (config.USER_DIR / "day24.txt").read_text()
    return ValleyMap.from_input_data(tuple(parse_map(input_data)))


def test_loop(simple_sample_map):
    valley_map = simple_sample_map
    seen_states = {}
    for i in range(1000):
        if valley_map.tornadoes in seen_states:
            assert i == 12
            break

        next_map = valley_map.next
        seen_states[valley_map.tornadoes] = next_map
        valley_map = next_map


def test_tornado_wrap_right():
    valley_map = ValleyMap.from_input_data(tuple(parse_map("# ##\n#.>#\n## #")))
    valley_map = valley_map.next
    assert valley_map.to_map() == "#.##\n#>.#\n##.#\n"


def test_tornado_wrap_left():
    valley_map = ValleyMap.from_input_data(tuple(parse_map("# ##\n#<.#\n## #")))
    valley_map = valley_map.next
    assert valley_map.to_map() == "#.##\n#.<#\n##.#\n"


def test_tornado_wrap_up():
    valley_map = ValleyMap.from_input_data(tuple(parse_map("# ##\n#.^#\n#..#\n## #\n")))
    valley_map = valley_map.next
    assert valley_map.to_map() == "#.##\n#..#\n#.^#\n##.#\n"


def test_tornado_wrap_down():
    valley_map = ValleyMap.from_input_data(tuple(parse_map("# ##\n#..#\n#.v#\n## #\n")))
    valley_map = valley_map.next
    assert valley_map.to_map() == "#.##\n#.v#\n#..#\n##.#\n"


def test_tornado_positions(super_simple_sample_map):
    valley_map = super_simple_sample_map

    print(valley_map)
    for _ in range(10):
        valley_map = valley_map.next
        print(valley_map)
