import re
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Dict, Iterable, Iterator, List, Mapping, NamedTuple, Set, Tuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich.progress import track

PTN_INPUT = re.compile(
    r"^Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


class Valve(NamedTuple):
    name: str
    rate: int


class GraphNode(NamedTuple):
    valve: Valve
    distance: int


class Graph(Mapping[Valve, Tuple[GraphNode]]):
    def __init__(self, graph: Mapping[Valve, Iterable[GraphNode]]):
        self._graph = [
            (k, tuple(v1 for v1 in sorted(v, key=lambda v1: v1.valve.name)))
            for k, v in graph.items()
        ]
        self._graph = tuple(sorted(self._graph, key=lambda v: v[0].name))

    @lru_cache
    def __getitem__(self, item: Valve) -> Tuple[GraphNode]:
        return next(v[1] for v in self._graph if v[0] == item)

    def __iter__(self) -> Iterator[Valve]:
        return iter([item[0] for item in self._graph])

    def __len__(self) -> int:
        return len(self._graph)

    def __hash__(self):
        return hash(self._graph)

    def __eq__(self, other):
        return self._graph == other._graph


class ValveRegistry(Mapping[str, Valve]):
    def __init__(self, input: str):
        valves_by_name = {}
        links_by_name = {}
        for line in input.splitlines():
            match = PTN_INPUT.match(line)
            if not match:
                raise ValueError(f"Invalid valve config: {line}")
            name, flow_rate, links = match.groups()
            valves_by_name[name] = Valve(name, int(flow_rate))
            links_by_name[name] = [l.strip() for l in links.split(",")]

        valves = {}
        for valve in valves_by_name.values():
            valves[valve] = [
                GraphNode(valves_by_name[link], 1) for link in links_by_name[valve.name]
            ]

        self.__graph = Graph(valves)
        self.__valves = valves_by_name

    @property
    def graph(self) -> Graph:
        return self.__graph

    def __getitem__(self, item: str) -> Valve:
        return self.__valves[item]

    def __getattr__(self, item) -> Valve:
        return self.__valves[item]

    def __len__(self) -> int:
        return len(self.__valves)

    def __iter__(self) -> Iterator[Valve]:
        return iter(self.__valves.values())


@lru_cache
def dijkstra(graph: Graph, source: Valve) -> Dict[Valve, int]:
    distances = {valve: float("inf") for valve in graph}
    distances[source] = 0
    unvisited = set(graph)

    # Repeat until all vertices are visited
    while unvisited:
        # Select the unvisited vertex with the smallest distance
        current = min(unvisited, key=lambda vertex: distances[vertex])

        # Update distances of neighbors
        for node in graph[current]:
            if node.valve in unvisited:
                distances[node.valve] = min(
                    distances[node.valve], distances[current] + node.distance
                )

        # Remove current from unvisited
        unvisited.remove(current)

    return distances


def find_paths(
    distances,
    active_valves: Set[Valve],
    open_valves: Set[Valve],
    current_valve,
    time_remaining,
) -> List[List[Tuple[Valve, int]]]:
    if time_remaining <= 0:
        return []
    if time_remaining == 1:
        return [[(current_valve, time_remaining - 1)]]

    time_remaining -= 1

    paths = [[(current_valve, time_remaining)]]
    for valve in active_valves - open_valves:
        paths.extend(
            [(current_valve, time_remaining), *p]
            for p in find_paths(
                distances,
                active_valves,
                open_valves | {valve},
                valve,
                time_remaining - distances[current_valve][valve],
            )
        )
    return paths


def get_score(path):
    return sum(v.rate * t for v, t in path)


def get_valves(path):
    return tuple(sorted([v for v, _ in path], key=lambda v: v.name))


def score_paths(paths):
    for p in paths:
        path_name = "->".join(v.name for v, _ in p)
        yield path_name, get_score(p)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day16(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day16.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day16.txt").read_text()

    valve_registry = ValveRegistry(input_data)

    active_valves = {valve for valve in valve_registry if valve.rate}
    distances = {}
    for valve in active_valves:
        distances[valve] = dijkstra(valve_registry.graph, valve)

    print("All distances calculated")

    paths = []
    aa_distances = dijkstra(valve_registry.graph, valve_registry.AA)
    for valve in active_valves:
        paths.extend(
            find_paths(
                distances, active_valves, {valve}, valve, 30 - aa_distances[valve]
            )
        )

    print("Paths", len(paths))

    scored_paths = list(score_paths(paths))
    scored_paths.sort(key=lambda p: p[1])
    for path_name, score in scored_paths[-5:]:
        print(score, path_name)

    print("Part 1:", scored_paths[-1][1])
    print()

    # Part 2

    p2_paths = []
    for valve in active_valves:
        p2_paths.extend(
            find_paths(
                distances, active_valves, {valve}, valve, 26 - aa_distances[valve]
            )
        )
    print("Calculated paths")

    p2_paths = list((get_valves(p), get_score(p)) for p in p2_paths)
    p2_paths.sort(key=lambda p: p[1], reverse=True)
    print("Sorted paths", len(p2_paths))

    highest_scoring_paths = {}
    for valves, score in p2_paths:
        if score > highest_scoring_paths.get(valves, 0):
            highest_scoring_paths[valves] = score

    print("Indexed paths", len(highest_scoring_paths))

    candidates = []
    for valves, score in highest_scoring_paths.items():
        # target_valves = active_valves - valves
        for v2, s2 in highest_scoring_paths.items():
            if not set(valves) & set(v2):
                candidates.append((valves + v2, score + s2))

    candidates.sort(key=lambda p: p[1])
    for valves, score in candidates[-10:]:
        print(score, "->".join(v.name for v in valves))
