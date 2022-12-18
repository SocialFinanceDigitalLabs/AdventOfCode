import pytest
from aoc_2022_kws.config import config
from aoc_2022_kws.day_17 import SPRITES, Chamber, Sprite, simulate_game


@pytest.fixture
def input_data():
    input_data = (config.USER_DIR / "day17.txt").read_text()
    return input_data


@pytest.fixture
def jet(input_data):
    return tuple(x for x in input_data if x in "<>")


@pytest.fixture
def sprites():
    return tuple(Sprite(s) for s in SPRITES)


def test_cycle(jet, sprites):
    cycle = 1745
    cycle_start = 72

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle)
    p2_1 = chamber.max_y

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle * 2)
    p2_2 = chamber.max_y

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle * 3)
    p2_3 = chamber.max_y

    height_per_cycle = p2_2 - p2_1
    start_height = p2_1 - height_per_cycle

    print("Start Height =", start_height)
    print("Height per cycle =", height_per_cycle)

    assert p2_3 == start_height + 3 * height_per_cycle


def test_cycle_and_increment(jet, sprites):
    cycle = 1745
    cycle_start = 72

    start_height = 106
    height_per_cycle = 2738

    target = 100_000

    cycles = (target - cycle_start) // cycle
    extra_cycles = (target - cycle_start) % cycle

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + extra_cycles)
    height_extra = chamber.max_y - start_height

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle * cycles + extra_cycles)
    height_test = chamber.max_y

    answer = start_height + height_per_cycle * cycles + height_extra
    print("ANSWER", answer)
    assert height_test == answer


def test_answer(jet, sprites):
    cycle = 1745
    cycle_start = 72

    start_height = 106
    height_per_cycle = 2738

    target = 1000000000000

    cycles = (target - cycle_start) // cycle
    extra_cycles = (target - cycle_start) % cycle

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + extra_cycles)
    height_extra = chamber.max_y - start_height

    answer = start_height + height_per_cycle * cycles + height_extra
    print("ANSWER", answer)
