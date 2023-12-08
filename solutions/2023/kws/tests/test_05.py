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


def test_all_ranges():
    mapper = Mapper("test-to-test map:", ["100 98 2", "52 50 5"])
    all_ranges = mapper.all_ranges

    assert len(all_ranges) == 5
    assert all_ranges[0].source_range_start == 0
    assert all_ranges[-1].source_range_end is None
    assert [x.source_range_start for x in all_ranges] == [0, 50, 55, 98, 100]


def test_all_ranges_no_gap():
    mapper = Mapper("test-to-test map:", ["100 98 2", "52 50 48"])
    all_ranges = mapper.all_ranges

    assert len(all_ranges) == 4
    assert all_ranges[0].source_range_start == 0
    assert all_ranges[-1].source_range_end is None
    assert [x.source_range_start for x in all_ranges] == [0, 50, 98, 100]


def test_ranges_within():
    mapper = Mapper("test-to-test map:", ["100 98 2", "52 50 5"])
    ranges = list(mapper.ranges_within(25, 60))
    assert len(ranges) == 3
    assert ranges[0].source_range_start == 25
    assert ranges[0].destination_range_start == 25
    assert ranges[1].source_range_start == 50
    assert ranges[1].destination_range_start == 52
    assert ranges[2].source_range_start == 55
    assert ranges[2].destination_range_start == 57
    assert ranges[2].source_range_end == 60

    ranges = list(mapper.ranges_within(95, 200))
    assert len(ranges) == 3

    starts = [x.source_range_start for x in ranges]
    assert starts == [95, 98, 100]
    ends = [x.source_range_end for x in ranges]
    assert ends == [97, 99, 200]


def test_reverse():
    mapper = Mapper("test-to-test map:", ["100 98 2", "52 50 48"])
    mapper = mapper.reverse

    assert [x.source_range_start for x in mapper.all_ranges] == [0, 52, 100, 102]


def test_merge():
    mapper_a = Mapper("a-to-b map:", ["100 50 10", "20 100 20"])
    mapper_b = Mapper("b-to-c map:", ["20 105 2", "200 30 10"])

    mapper_c = mapper_a.merge(mapper_b)

    assert mapper_a.get(55) == 105
    assert mapper_b.get(105) == 20
    assert mapper_c.get(55) == 20

    assert mapper_c.get(0) == 0
    assert mapper_c.get(300) == 300

    all_ranges = mapper_c.all_ranges
    all_ranges.sort(key=lambda x: x.destination_range_start)

    assert all_ranges[1].destination_range_start == 20
