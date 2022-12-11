from aoc_2022_kws.day_06 import part1, part2

part1_samples = [
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]

part2_samples = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
]


def test_part1():
    assert part1(part1_samples[0]) == 5
    assert part1(part1_samples[1]) == 6
    assert part1(part1_samples[2]) == 10
    assert part1(part1_samples[3]) == 11


def test_part2():
    for text, answer in part2_samples:
        assert part2(text) == answer
