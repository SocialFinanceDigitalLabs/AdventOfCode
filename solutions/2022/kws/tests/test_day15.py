from aoc_2022_kws.day_15 import Range, reduce_ranges


def test_merge_ranges():
    ranges_in_row = reduce_ranges(
        [
            Range(min=-8, max=12),
            Range(min=6, max=10),
            Range(min=12, max=14),
            Range(min=14, max=26),
        ]
    )
    assert ranges_in_row == [Range(min=-8, max=26)]

    ranges_in_row = reduce_ranges(
        [
            Range(min=1, max=3),
            Range(min=10, max=14),
            Range(min=14, max=14),
            Range(min=4, max=12),
            Range(min=-2, max=2),
            Range(min=14, max=26),
            Range(min=16, max=16),
        ]
    )
    assert ranges_in_row == [Range(min=-2, max=26)]
