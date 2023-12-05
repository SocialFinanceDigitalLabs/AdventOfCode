from aoc_2023_kws.day_05 import Mapper, UberMapper


def test_mapper():
    mapper = Mapper("test-to-test map:", ["50 98 2"])
    assert mapper.get(97) == 97
    assert mapper.get(98) == 50
    assert mapper.get(99) == 51
    assert mapper.get(100) == 100


def test_mapper_length_1():
    mapper = Mapper("test-to-test map:", ["50 98 1"])
    assert mapper.get(97) == 97
    assert mapper.get(98) == 50
    assert mapper.get(99) == 99
    assert mapper.get(100) == 100


def test_mapper_length_0():
    mapper = Mapper("test-to-test map:", ["50 98 0"])
    assert mapper.get(97) == 97
    assert mapper.get(98) == 98
    assert mapper.get(99) == 99
    assert mapper.get(100) == 100


def test_mapper_smaller():
    mapper = Mapper("test-to-test map:", ["98 50 2"])
    assert mapper.get(49) == 49
    assert mapper.get(50) == 98
    assert mapper.get(51) == 99
    assert mapper.get(52) == 52


def test_mapper_min():
    mapper = Mapper("test-to-test map:", ["100 98 2", "52 50 48"])
    assert mapper.min_mapped == 50
    assert mapper.min_target == 52
