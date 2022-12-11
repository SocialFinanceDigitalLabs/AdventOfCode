# Advent of Code 2021 Day 22

class Box:

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.x2 = min(x1, x2), max(x1, x2)
        self.y1, self.y2 = min(y1, y2), max(y1, y2)
        self.z1, self.z2 = min(z1, z2), max(z1, z2)

    def intersects(self, other: "Box") -> bool:
        return (
            self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1 and
            self.z1 <= other.z2 and self.z2 >= other.z1
        )

    # Returns a Box that is the intersection of self and other
    def intersect(self, other: "Box") -> "Box":
        if not self.intersects(other):
            raise ValueError("The boxes do not intersect")
        return Box(
            max(self.x1, other.x1),
            min(self.x2, other.x2),
            max(self.y1, other.y1),
            min(self.y2, other.y2),
            max(self.z1, other.z1),
            min(self.z2, other.z2)
        )

    def __eq__(self, other):
        return (
            other is not None and
            self.x1 == other.x1 and self.x2 == other.x2 and
            self.y1 == other.y1 and self.y2 == other.y2 and
            self.z1 == other.z1 and self.z2 == other.z2
        )

    def __repr__(self):
        return f"x={self.x1}..{self.x2}, y={self.y1}..{self.y2}, z={self.z1}..{self.z2}"


class StateBox(Box):

    def __init__(self, x1, x2, y1, y2, z1, z2, state):
        super().__init__(x1, x2, y1, y2, z1, z2)
        self.state = state

    def __repr__(self):
        return f"{'on' if self.state else 'off'} {super().__repr__()}"

    @classmethod
    def from_input(cls, x, y , z, value) -> "StateBox":
        return cls(*x, *y, *z, value)


def split_coords(coord, value):
    c, value = value.split('=', 1)
    assert c == coord
    start, end = value.split('..')
    return int(start), int(end)


def parse_input(value):
    state, coords = value.split(' ', 1)
    coords = coords.split(',')
    x = split_coords('x', coords[0])
    y = split_coords('y', coords[1])
    z = split_coords('z', coords[2])
    return x, y , z, 1 if state == 'on' else 0


def limit(min_value, max_value, min_range, max_range):
    min_value, max_value = min(min_value, max_value), max(min_value, max_value)
    if max_value < min_range or min_value > max_range:
        return None
    return max(min_value, min_range), min(max_value, max_value)
