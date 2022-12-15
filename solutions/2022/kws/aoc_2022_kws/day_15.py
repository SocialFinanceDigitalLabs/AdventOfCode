import re
from typing import Generator, Iterable, List, NamedTuple, Optional, Set, Tuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit
from rich.progress import track

CFG_PTN = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


class Range(NamedTuple):
    """
    Covers a range of values, inclusive.
    """

    min: int
    max: int

    def overlap(self, other: "Range") -> Optional["Range"]:
        """
        If the two sensors overlap, return the combined x_min and x_max for the new coverage,
        otherwise return None
        :param other:
        :return:
        """
        if self.min > other.max or self.max < other.min:
            return None
        return Range(min(self.min, other.min), max(self.max, other.max))


class Sensor:
    def __init__(self, cfg: str):
        m = CFG_PTN.match(cfg)
        self.x, self.y, self.beacon_x, self.beacon_y = map(int, m.groups())

        self.distance = abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)
        self.x_min = self.x - self.distance
        self.x_max = self.x + self.distance
        self.y_min = self.y - self.distance
        self.y_max = self.y + self.distance

    def coverage_for_y(self, y: int) -> Set[int]:
        range_x = self.range_for_y(y)
        return set(range(range_x.min, range_x.max + 1))

    def range_for_y(self, y: int) -> Range:
        dx = self.distance - abs(y - self.y)
        return Range(self.x - dx, self.x + dx)

    @property
    def covered_area(self) -> Generator[Tuple[int, int], None, None]:
        for y in range(self.y_min, self.y_max + 1):
            for x in self.coverage_for_y(y):
                yield x, y

    def __repr__(self):
        return f"Sensor({self.x}, {self.y})"


def reduce_ranges(ranges: Iterable[Range]) -> List[Range]:
    ranges = list(ranges)
    if len(ranges) < 2:
        return ranges

    ranges.sort(key=lambda r: r.min, reverse=True)
    merged = []

    r_1 = ranges.pop()
    r_2 = ranges.pop()
    while r_2:
        if r_1.max + 1 >= r_2.min:
            r_1 = Range(r_1.min, max(r_1.max, r_2.max))
            r_2 = ranges.pop() if ranges else None
        else:
            merged.append(r_1)
            r_1 = r_2
            r_2 = ranges.pop() if ranges else None
    merged.append(r_1)
    return merged


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day15(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day15.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day15.txt").read_text()

    sensors = [Sensor(line) for line in input_data.splitlines()]

    print("All sensors", sensors)

    test_y = 10 if sample else 2_000_000

    sensors_covering_row = [s for s in sensors if s.y_min <= test_y <= s.y_max]
    coverage_y = set()
    for s in sensors_covering_row:
        coverage_y.update(s.coverage_for_y(test_y))
    coverage_y -= set([s.x for s in sensors if s.y == test_y])
    coverage_y -= set(
        [s.beacon_x for s in sensors_covering_row if s.beacon_y == test_y]
    )

    part_1 = len(coverage_y)
    print("Part 1", part_1)

    # Part 2
    max_search = 20 if sample else 4_000_000

    for y in track(range(max_search + 1)):
        sensors_covering_row = [s for s in sensors if s.y_min <= y <= s.y_max]
        ranges_in_row = reduce_ranges([s.range_for_y(y) for s in sensors_covering_row])

        if len(ranges_in_row) == 2:
            print(f"Found multiple ranges at y={y}: {ranges_in_row}")
            # Making the assumption here that there is a single gap between the two ranges
            x = ranges_in_row[0].max + 1
            print(f"Frequency {x} * 4,000,000 + {y} = {x*4_000_000 + y}")
        elif len(ranges_in_row) > 2:
            print("Found too many ranges", y, ranges_in_row)
        else:
            row_range = ranges_in_row[0]
            if row_range.min > 0 or row_range.max < max_search:
                print("Found limited range", y, row_range)
