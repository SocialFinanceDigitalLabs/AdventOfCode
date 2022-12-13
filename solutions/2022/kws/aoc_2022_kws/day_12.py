from collections import namedtuple
from typing import Dict, List, NamedTuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit


class Coordinate(NamedTuple):
    x: int
    y: int


class Point(NamedTuple):
    coord: Coordinate
    name: str

    @property
    def height(self):
        if self.name == "S":
            return "a"
        elif self.name == "E":
            return "z"
        else:
            return self.name


def dijkstra(graph: Dict[Point, List[Point]], source: Point):
    # Initialize distances and set all vertices as unvisited
    distances = {vertex: float("inf") for vertex in graph}
    distances[source] = 0
    unvisited = set(graph)

    # Repeat until all vertices are visited
    while unvisited:
        # Select the unvisited vertex with the smallest distance
        current = min(unvisited, key=lambda vertex: distances[vertex])

        # Update distances of neighbors
        for neighbor in graph[current]:
            if neighbor in unvisited:
                distances[neighbor] = min(distances[neighbor], distances[current] + 1)

        # Remove current from unvisited
        unvisited.remove(current)

    return distances


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day12(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day12.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day12.txt").read_text()

    terrain_map = {}
    neighbour_map = {}
    start: Point = None
    end: Point = None

    # parse the input data
    for y, line in enumerate(input_data.splitlines()):
        for x, char in enumerate(line):
            coord = Coordinate(x, y)
            point = Point(coord, char)
            terrain_map[coord] = point
            if char == "S":
                start = point
            elif char == "E":
                end = point

    # build the graph
    for coord, point in terrain_map.items():
        neighbours = [
            terrain_map.get(Coordinate(coord.x + 1, coord.y)),
            terrain_map.get(Coordinate(coord.x - 1, coord.y)),
            terrain_map.get(Coordinate(coord.x, coord.y + 1)),
            terrain_map.get(Coordinate(coord.x, coord.y - 1)),
        ]
        neighbours = [n for n in neighbours if n is not None]
        neighbours = [n for n in neighbours if ord(n.height) - ord(point.height) < 2]

        neighbour_map[point] = neighbours

    print("Finding path from", start, end)
    print("Neighbours start:", neighbour_map[start])
    print("Neighbours end:", neighbour_map[end])

    distances = dijkstra(neighbour_map, start)
    print("PART1", distances[end])

    # We now need to reverse the rules for possible routes down
    for coord, point in terrain_map.items():
        neighbours = [
            terrain_map.get(Coordinate(coord.x + 1, coord.y)),
            terrain_map.get(Coordinate(coord.x - 1, coord.y)),
            terrain_map.get(Coordinate(coord.x, coord.y + 1)),
            terrain_map.get(Coordinate(coord.x, coord.y - 1)),
        ]
        neighbours = [n for n in neighbours if n is not None]
        neighbours = [n for n in neighbours if ord(point.height) - ord(n.height) < 2]

        neighbour_map[point] = neighbours

    distances = dijkstra(neighbour_map, end)
    a_dist = [(p, d) for p, d in distances.items() if p.height == "a"]
    print("PART2", min(a_dist, key=lambda x: x[1]))


if __name__ == "__main__":
    day12()
