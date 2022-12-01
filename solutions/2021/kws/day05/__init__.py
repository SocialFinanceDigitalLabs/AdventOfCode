# Advent of Code 2021 Day 5
import functools
from collections import namedtuple

import numpy as np

Coords = namedtuple('Coords', 'x y')


class Vent:
    def __init__(self, start, end, max_dim=None):
        self.start = start
        self.end = end
        if max_dim:
            self.dimension = max_dim + 1
        else:
            self.dimension = max(max(start.x, end.x), max(start.y, end.y)) + 1
        self.map = np.array([[0]*self.dimension]*self.dimension, dtype=int)

        change_x = end.x - start.x
        change_y = end.y - start.y
        change = max(abs(change_y), abs(change_x))

        for step in range(0, change+1):
            x = start.x + (change_x/change*step)
            y = start.y + (change_y/change*step)
            self.map[int(y),int(x)] = 1

    def __str__(self):
        return self.to_map(self.map)

    @property
    def straight(self):
        return self.start.x == self.end.x or self.start.y == self.end.y

    @classmethod
    def coords_from_string(cls, string):
        start, end = string.split('->')
        return Coords(*map(int, start.split(','))),  Coords(*map(int, end.split(',')))

    @classmethod
    def from_string(cls, string, max_dim=None):
        x, y = cls.coords_from_string(string)
        return cls(x, y, max_dim=max_dim)

    @staticmethod
    def add(*vents):
        return functools.reduce(lambda a, b: a + b, [v.map for v in vents])

    @staticmethod
    def to_map(map) -> str:
        lines = []
        for row in map:
            lines.append(''.join([str(x) if x else '.' for x in row]))
        return '\n'.join(lines)


def parse_input(lines):
    max_dim = 0
    for line in lines:
        x, y = Vent.coords_from_string(line)
        max_dim = max(max_dim, max(x.x, x.y), max(y.x, y.y))
    for line in lines:
        yield Vent.from_string(line, max_dim=max_dim)



