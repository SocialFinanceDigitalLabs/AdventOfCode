import pytest
from aoc_2022_kws.config import config
from aoc_2022_kws.day_16 import (
    GraphNode,
    ValveRegistry,
    dijkstra,
    find_path,
    score_paths,
    simplify_graph,
)


@pytest.fixture
def sample1():
    return """
Valve AA has flow rate=0; tunnels lead to valves BB, CC
Valve BB has flow rate=13; tunnels lead to valves AA
Valve CC has flow rate=2; tunnels lead to valves AA
""".strip()


@pytest.fixture
def sample_puzzle():
    return (config.SAMPLE_DIR / "day16.txt").read_text()


def test_registry(sample1):
    valve_registry = ValveRegistry(sample1)
    assert len(valve_registry) == 3

    AA = valve_registry.AA
    assert AA.rate == 0

    assert valve_registry.graph[AA] == (
        GraphNode(valve_registry.BB, 1),
        GraphNode(valve_registry.CC, 1),
    )


def test_dijkstra(sample1):
    valve_registry = ValveRegistry(sample1)
    distances = dijkstra(valve_registry.graph, valve_registry.AA)

    assert distances[valve_registry.AA] == 0
    assert distances[valve_registry.BB] == 1
    assert distances[valve_registry.CC] == 1

    distances = dijkstra(valve_registry.graph, valve_registry.BB)
    assert distances[valve_registry.CC] == 2


def test_find_path(sample1):
    valve_registry = ValveRegistry(sample1)

    paths = find_path(valve_registry.graph, valve_registry.AA, 30)
    paths = sorted(score_paths(paths), reverse=True)

    assert paths[0] == (414, "AA/BB/CC")
    assert paths[1] == (381, "AA/CC/BB")
    assert paths[2] == (364, "AA/BB")


def test_simplify_graph(sample1):
    valve_registry = ValveRegistry(sample1)
    graph = valve_registry.graph

    assert len(graph) == 3
    assert graph[valve_registry.BB] == (GraphNode(valve_registry.AA, 1),)

    distances = dijkstra(graph, valve_registry.BB)
    assert distances[valve_registry.AA] == 1
    assert distances[valve_registry.CC] == 2

    simple_graph = simplify_graph(graph, {})

    assert len(simple_graph) == 2
    assert simple_graph[valve_registry.BB] == (GraphNode(valve_registry.CC, 2),)

    distances = dijkstra(simple_graph, valve_registry.BB)
    assert valve_registry.AA not in distances
    assert distances[valve_registry.CC] == 2


def test_simplify_graph_more_complex():
    sample = """
Valve AA has flow rate=0; tunnels lead to valves AB, AD
Valve AB has flow rate=0; tunnels lead to valves AA, BC
Valve BC has flow rate=2; tunnels lead to valves AB
Valve AD has flow rate=2; tunnels lead to valves AA
""".strip()
    valve_registry = ValveRegistry(sample)
    graph = valve_registry.graph

    assert len(graph) == 4

    simple_graph = simplify_graph(graph, {})

    assert len(simple_graph) == 2
    assert simple_graph[valve_registry.BC] == (GraphNode(valve_registry.AD, 3),)
    assert simple_graph[valve_registry.AD] == (GraphNode(valve_registry.BC, 3),)

    simple_graph_with_origin = simplify_graph(graph, {}, keep=valve_registry.AA)
    assert len(simple_graph_with_origin) == 3
    assert simple_graph_with_origin[valve_registry.BC] == (
        GraphNode(valve_registry.AA, 2),
    )
    assert simple_graph_with_origin[valve_registry.AD] == (
        GraphNode(valve_registry.AA, 1),
    )


def test_simplify_graph_from_puzzle(sample_puzzle):
    valve_registry = ValveRegistry(sample_puzzle)
    graph = valve_registry.graph

    assert len(graph) == 10
    assert graph[valve_registry.HH] == (GraphNode(valve_registry.GG, 1),)

    simple_graph = simplify_graph(graph, {})

    assert len(simple_graph) == 6
    assert simple_graph[valve_registry.HH] == (GraphNode(valve_registry.EE, 3),)

    distances = dijkstra(graph, valve_registry.HH)
    assert distances[valve_registry.JJ] == 7

    distances = dijkstra(simple_graph, valve_registry.HH)
    assert distances[valve_registry.JJ] == 7


def test_simplify_input():
    input = (config.USER_DIR / "day16.txt").read_text()
    valve_registry = ValveRegistry(input)
    graph = valve_registry.graph

    simple_graph = simplify_graph(graph, {}, keep=valve_registry.AA)

    for valve, neighbours in simple_graph.items():
        print(
            f"Valve {valve.name} has flow rate={valve.rate}; "
            f"tunnels lead to valves {', '.join([f'{n.valve.name}({n.distance})' for n in neighbours])}"
        )

    nodes_to_consider = sorted([node for node in graph if node.rate > 0])
    for node in nodes_to_consider:
        original_distances = dijkstra(graph, node)
        simple_distances = dijkstra(simple_graph, node)
        for link in nodes_to_consider:
            print(
                f"{node.name} -> {link.name}: {original_distances[link]} -> {simple_distances[link]}"
            )
            assert original_distances[link] == simple_distances[link]
