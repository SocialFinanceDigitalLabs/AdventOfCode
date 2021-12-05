# Advent of Code 2021 Day 5
import numpy as np

from common import standard_setup
import day05


def main(*argv):
    lines = standard_setup(*argv)
    vents = list(day05.parse_input(lines))

    straight_vents = [v for v in vents if v.straight]

    print(f'Parsed {len(vents)} vents, of which {len(straight_vents)} are either horizontal or vertical.')

    map = day05.Vent.add(*straight_vents)
    print(f"There are {np.count_nonzero(map > 1)} intersections.")

    map = day05.Vent.add(*vents)
    print(f"There are {np.count_nonzero(map > 1)} intersections for all lines.")


if __name__ == "__main__":
    main()

