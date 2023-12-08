import re
from collections import namedtuple

import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit

PTN_MATCHER = re.compile(r"(\w+)-to-(\w+) map:")


class Range:
    def __init__(self, destination_range_start, source_range_start, range_length):
        self._destination_range_start = destination_range_start
        self._source_range_start = source_range_start
        self._range_length = range_length

    @property
    def destination_range_start(self):
        return self._destination_range_start

    @property
    def destination_range_end(self):
        """
        This is the last value within the range, so this is INCLUSIVE
        """
        if self._range_length is None:
            return None
        return self._destination_range_start + self._range_length - 1

    @property
    def source_range_start(self):
        return self._source_range_start

    @property
    def source_range_end(self):
        """
        This is the last value within the range, so this is INCLUSIVE
        """
        if self._range_length is None:
            return None
        return self._source_range_start + self._range_length - 1

    @property
    def range_length(self):
        return self._range_length

    def in_source_range(self, value):
        return self.source_range_start <= value <= self.source_range_end

    def in_destination_range(self, value):
        return self.destination_range_start <= value <= self.destination_range_end

    def __repr__(self):
        return f"Range<{self._destination_range_start, self._source_range_start, self._range_length}>"

    def __lt__(self, other):
        return self.source_range_start < other.source_range_start


class Mapper:
    def __init__(self, mapper_id, input_data):
        matches = PTN_MATCHER.match(mapper_id)
        self.from_id = matches.group(1)
        self.to_id = matches.group(2)
        self._ranges = []
        while input_data and input_data[0].strip():
            current_line = input_data.pop(0).strip()
            (
                destination_range_start,
                source_range_start,
                range_length,
            ) = current_line.split(" ", 3)
            destination_range_start = int(destination_range_start)
            source_range_start = int(source_range_start)
            range_length = int(range_length)
            self._ranges.append(
                Range(destination_range_start, source_range_start, range_length)
            )
        self._ranges.sort()

    def get(self, value):
        for r in self._ranges:
            if r.source_range_start <= value < r.source_range_start + r.range_length:
                return r.destination_range_start + value - r.source_range_start
        return value

    @property
    def all_ranges(self):
        """
        Returns all ranges, including the 'ranges' between the ranges (straight through mappings)
        """
        source_ranges = list(self._ranges)
        ranges = []
        for i in range(len(source_ranges)):
            current_range = source_ranges[i]
            if i == 0 and current_range.source_range_start > 0:
                ranges.append(Range(0, 0, current_range.source_range_start))
            else:
                previous_range = source_ranges[i - 1]
                gap_length = (
                    current_range.source_range_start
                    - previous_range.source_range_end
                    - 1
                )
                if gap_length > 0:
                    ranges.append(
                        Range(
                            previous_range.destination_range_end + 1,
                            previous_range.source_range_end + 1,
                            gap_length,
                        )
                    )
            ranges.append(
                Range(
                    current_range.destination_range_start,
                    current_range.source_range_start,
                    current_range.range_length,
                )
            )
        ranges.append(
            Range(
                ranges[-1].source_range_end + 1, ranges[-1].source_range_end + 1, None
            )
        )
        return ranges

    def ranges_within(self, source_start, source_end):
        """
        Returns all ranges that are within the given source range (inclusive)
        """
        if source_end is None:
            return []

        for range in self.all_ranges:
            if range.source_range_start > source_end or (
                range.source_range_end and range.source_range_end < source_start
            ):
                continue
            range_start = max(range.source_range_start, source_start)
            range_start_delta = range_start - range.source_range_start
            range_end = (
                source_end
                if range.source_range_end is None
                else min(range.source_range_end, source_end)
            )

            yield Range(
                range.destination_range_start + range_start_delta,
                range_start,
                range_end - range_start + 1,
            )

    def merge(self, destionation_mapper: "Mapper"):
        """
        Takes the given destination and returns a mapper that maps from the source of this mapper
        to the destination of the given mapper.
        """
        assert self.to_id == destionation_mapper.from_id

        source_ranges = list(self.all_ranges)

        mapped_ranges = []
        for r in source_ranges:
            dest_ranges = destionation_mapper.ranges_within(
                r.destination_range_start, r.destination_range_end
            )
            for dr in dest_ranges:
                offset = dr.source_range_start - r.destination_range_start
                mapped_ranges.append(
                    Range(
                        dr.destination_range_start,
                        r.source_range_start + offset,
                        dr.range_length,
                    )
                )

        mapper = Mapper(f"{self.from_id}-to-{destionation_mapper.to_id} map:", [])
        mapper._ranges = mapped_ranges
        mapper._ranges.sort()
        return mapper

    @property
    def reverse(self):
        reverse_mapper = Mapper(f"{self.to_id}-to-{self.from_id} map:", [])
        reverse_mapper._ranges = [
            Range(
                x.source_range_start,
                x.destination_range_start,
                x.range_length,
            )
            for x in self._ranges
        ]
        reverse_mapper._ranges.sort()
        return reverse_mapper

    @property
    def min_mapped(self):
        return min([x[1] for x in self._ranges])

    @property
    def max_mapped(self):
        return max([x[1] for x in self._ranges])

    @property
    def min_target(self):
        return min([x[0] for x in self._ranges])

    @property
    def max_target(self):
        return max([x[0] for x in self._ranges])

    def __repr__(self):
        return f"<Mapper {self.from_id} to {self.to_id}>"


class UberMapper:
    def __init__(self, mappers):
        self.mappers = {m.from_id: m for m in mappers}

    def get(self, from_id, to_id, value):
        mappings = [(from_id, value)]
        while True:
            next_mapper = self.mappers[from_id]
            from_id = next_mapper.to_id
            value = next_mapper.get(value)
            mappings.append((from_id, value))
            if next_mapper.to_id == to_id:
                return mappings[-1][1], mappings

    @property
    def reverse(self):
        return UberMapper([m.reverse for m in self.mappers.values()])

    def merge(self, from_id, to_id):
        mapper = self[from_id]
        while mapper.to_id != to_id:
            mapper = mapper.merge(self[mapper.to_id])
        return mapper

    def __getitem__(self, key):
        return self.mappers[key]


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day05(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day05.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day05.txt").read_text()

    parse_input(input_data)


def parse_input(input_data):
    input_data = input_data.strip().splitlines()

    seeds = input_data.pop(0)[6:].strip().split(" ")
    seeds = [int(x) for x in seeds if x]

    all_mappers = []

    while input_data:
        current_line = input_data.pop(0).strip()
        if not current_line:
            continue

        if ":" in current_line:
            mapper = Mapper(current_line, input_data)
            all_mappers.append(mapper)

    uber_mapper = UberMapper(all_mappers)

    print(seeds, all_mappers)

    # Part 1
    all_locations = []
    for seed in seeds:
        soil_id, mappers = uber_mapper.get("seed", "location", seed)
        print(f"Seed {seed} needs location {soil_id}")
        all_locations.append((soil_id, mappers))

    all_locations.sort(key=lambda x: x[0])

    print(f"Part 1: {all_locations[0]}")

    # Part 2
    part2_reverse_deep(seeds, uber_mapper)


def part2_reverse_deep(seeds, uber_mapper):
    mapper = uber_mapper.merge("seed", "location")

    all_ranges = mapper.all_ranges
    all_ranges.sort(key=lambda x: x.destination_range_start)

    print(f"Testing {len(all_ranges)} mapped ranges")

    seed_ranges = []
    for seed_ix in range(0, len(seeds), 2):
        seed_ranges.append((seeds[seed_ix], seeds[seed_ix] + seeds[seed_ix + 1]))

    def get_seeds(start_value, end_value):
        for seed_start, seed_end in seed_ranges:
            if seed_start <= end_value and seed_end >= start_value:
                return (seed_start, seed_end)

    for r in all_ranges:
        seed_range = get_seeds(r.source_range_start, r.source_range_end)
        if seed_range:
            min_seed = max(seed_range[0], r.source_range_start)
            target = mapper.get(min_seed)
            print(f"Location {target} can be reached by seed {min_seed}")
            return
        else:
            print("No seed range found for", r)


def part2_brute_force(seeds, uber_mapper):
    seed_ranges = []
    for seed_ix in range(0, len(seeds), 2):
        seed_ranges.append((seeds[seed_ix], seeds[seed_ix] + seeds[seed_ix + 1]))
    print(seed_ranges)

    def in_range(value):
        for seed_range in seed_ranges:
            if seed_range[0] <= value <= seed_range[1]:
                return True
        return False

    reverse = uber_mapper.reverse
    for loc in range(0, 100_000_000):
        if loc % 25_000 == 0:
            print(f"Checking location {loc}")
        seed_id, _ = reverse.get("location", "seed", loc)
        if in_range(seed_id):
            print(f"Location {loc} can be reached by seed {seed_id}")
            break
