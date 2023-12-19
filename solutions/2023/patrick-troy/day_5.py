from aocd import get_data
from functools import reduce

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

seeds, *mappings = get_data(day=5, year=2023, session=session).split("\n\n")
test_seeds, *test_mappings = open("solutions/2023/patrick-troy/samples/day_5_1.txt").read().split("\n\n")


def _map_seeds(seeds):
    return map(int, seeds.split()[1:])


def _lookup(seed_start, mapping):
    for m in mapping.split('\n')[1:]:
        dest_start, source_start, length = map(int, m.split())
        delta = seed_start - source_start
        if delta in range(length):
            return dest_start + delta
    else:
        return seed_start


def solve_1(seeds, mappings):
    seeds = _map_seeds(seeds)
    return min(reduce(_lookup, mappings, int(s)) for s in seeds)


assert solve_1(test_seeds, test_mappings) == 35
print(solve_1(seeds, mappings))


def _lookup_2(seed_start, mapping):
    for start, range in seed_start:
        while range > 0:
            for m in mapping.split('\n')[1:]:
                dest_start, source_start, length = map(int, m.split())
                delta = start - source_start
                if delta in range(length):
                    length = min(length - delta, range)
                    yield dest_start + delta, length
                    start += length
                    range -= length
                    break
            else:
                yield start, range
                break


def solve_2(seeds, mappings):
    seeds = list(_map_seeds(seeds))
    all_seeds = []
    for row in [[*range(s[0], s[0]+s[1])] for s in zip(seeds[0::2], seeds[1::2])]:
        all_seeds.extend(row)
    return min(reduce(_lookup, mappings, int(s)) for s in all_seeds)


assert solve_2(test_seeds, test_mappings) == 46
print(solve_2(seeds, mappings))
