from collections import defaultdict

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit


class Point:
    def __init__(self, grid: "Grid", row, col, char):
        self.grid = grid
        self.row = row
        self.col = col
        self.char = char
        self.region = None

    def __fill_point(self, point):
        if point is None or point.region is not None:
            return
        if point.char != self.char:
            return
        yield from point.fill(self.region)

    def fill(self, region):
        self.region = region
        yield self
        yield from self.__fill_point(self.left)
        yield from self.__fill_point(self.up)
        yield from self.__fill_point(self.right)
        yield from self.__fill_point(self.down)

    @property
    def left(self):
        return self.grid.get(self.row, self.col - 1)

    @property
    def right(self):
        return self.grid.get(self.row, self.col + 1)

    @property
    def up(self):
        return self.grid.get(self.row - 1, self.col)

    @property
    def down(self):
        return self.grid.get(self.row + 1, self.col)

    @property
    def has_top_fence(self):
        return not self.up or self.up.region != self.region

    @property
    def has_bottom_fence(self):
        return not self.down or self.down.region != self.region

    @property
    def has_left_fence(self):
        return not self.left or self.left.region != self.region

    @property
    def has_right_fence(self):
        return not self.right or self.right.region != self.region

    @property
    def fences(self):
        fences = 0
        if self.has_left_fence:
            fences += 1
        if self.has_right_fence:
            fences += 1
        if self.has_top_fence:
            fences += 1
        if self.has_bottom_fence:
            fences += 1
        return fences

    @property
    def fence_coordinates(self):
        # For a point at 0,0 the edges have coordinates: 0,0 1,0 1,1, 0,1
        if self.has_top_fence:
            yield ((self.col, self.row), (self.col + 1, self.row), "T")
        if self.has_bottom_fence:
            yield ((self.col, self.row + 1), (self.col + 1, self.row + 1), "B")
        if self.has_left_fence:
            yield ((self.col, self.row), (self.col, self.row + 1), "L")
        if self.has_right_fence:
            yield ((self.col + 1, self.row), (self.col + 1, self.row + 1), "R")

    def __repr__(self):
        return f"Point({self.row}, {self.col}, {self.char}, {self.fences})"


class Grid:
    def __init__(self, input_data):
        grid = []
        for row, line in enumerate(input_data.splitlines()):
            grid.append([])
            for col, char in enumerate(line):
                grid[row].append(Point(self, row, col, char))
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.regions = defaultdict(list)
        region = 0

        for r in range(self.rows):
            for c in range(self.cols):
                point = self.grid[r][c]
                if point.region is None:
                    self.regions[region].extend(point.fill(region))
                    region += 1

        print(f"Found {region} regions")

    def get(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return None
        return self.grid[row][col]


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day12(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day12.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day12.txt").read_text()

    grid = Grid(input_data)
    for region, points in grid.regions.items():
        print(region, points)
        print()

    total = 0
    for region in grid.regions:
        points = grid.regions[region]
        letter = points[0].char
        fences = 0
        for point in points:
            fences += point.fences
        area = len(points)
        score = fences * area
        total += score

        print(
            f"Region {region} of size {area} and letter {letter} has {fences} fences and score {score}"
        )

    print(f"Total score: {total}")

    if not sample:
        submit(total, part="a", day=12, year=2024)

    cost = 0
    for region_id, region in grid.regions.items():
        boundaries = set()
        for point in region:
            boundaries.update(point.fence_coordinates)
        merged_boundaries = merge_boundaries(boundaries)
        print(
            f"Region {region_id}{region[0].char} has area {len(region)} and {len(merged_boundaries)} boundaries\n"
        )
        cost += len(merged_boundaries) * len(region)

    print(f"Total cost: {cost}")
    if not sample:
        submit(cost, part="b", day=12, year=2024)


def merge_boundaries(boundaries):
    # Separate horizontal and vertical lines
    horizontal = [c for c in boundaries if c[2] in "TB"]
    vertical = [c for c in boundaries if c[2] in "LR"]

    # Merge horizontal lines
    horizontal.sort(key=lambda x: (x[0][1], x[0][0]))
    vertical.sort(key=lambda x: (x[0][0], x[0][1]))

    merged_horizontal = []
    while horizontal:
        current = horizontal.pop(0)
        next = horizontal[0] if horizontal else None
        if next is None:
            print(f" H Not merging lonely {current} - pushing {current} as completed\n")
            merged_horizontal.append(current)
            break
        if current[1] == next[0] and current[2] == next[2]:
            print(f" H Merging {current} and {next} => {current[0], next[1]}")
            horizontal[0] = (current[0], next[1], current[2])
        else:
            print(
                f" H Not merging {current} and {next} - pushing {current} as completed\n"
            )
            merged_horizontal.append(current)
            horizontal[0] = next

    # Merge vertical lines
    merged_vertical = []
    while vertical:
        current = vertical.pop(0)
        next = vertical[0] if vertical else None
        if next is None:
            print(f" V Not merging lonely {current} - pushing {current} as completed\n")
            merged_vertical.append(current)
            break
        if current[1] == next[0] and current[2] == next[2]:
            print(f" V Merging {current} and {next} => {current[0], next[1]}")
            vertical[0] = (current[0], next[1], current[2])
        else:
            print(
                f" V Not merging {current} and {next} - pushing {current} as completed\n"
            )
            merged_vertical.append(current)
            vertical[0] = next

    return merged_horizontal + merged_vertical
