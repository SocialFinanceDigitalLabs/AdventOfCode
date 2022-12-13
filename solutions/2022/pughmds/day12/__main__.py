EXPECTED_TEST_ANSWER_PART1 = [31]
EXPECTED_TEST_ANSWER_PART2 = [29]

"""
This is incredibly slow and unoptimised (and a bit hacky)
but...it gives the right answer, so...
I'll leave it for reference, but it could DEFINITELY be
optimised to speed things up by quite a bit.

Prepare to wait a few minutes on part 2...
"""


class Dijkstra:
    """
    Found Here: https://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
    """

    def __init__(self, vertices, graph):
        self.vertices = vertices
        self.graph = graph

    def find_route(self, start, end):
        unvisited = {n: float("inf") for n in self.vertices}
        unvisited[start] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex = min(unvisited, key=unvisited.get)  # get smallest distance
            for neighbour, _ in self.graph.get(min_vertex, {}).items():
                if neighbour in visited:
                    continue
                new_distance = unvisited[min_vertex] + self.graph[min_vertex].get(
                    neighbour, float("inf")
                )
                if new_distance < unvisited[neighbour]:
                    unvisited[neighbour] = new_distance
                    parents[neighbour] = min_vertex
            visited[min_vertex] = unvisited[min_vertex]
            unvisited.pop(min_vertex)
            if min_vertex == end:
                break
        return parents, visited

    @staticmethod
    def generate_path(parents, start, end):
        path = [end]
        while True:
            try:
                key = parents[path[0]]
                path.insert(0, key)
            except:
                return -1
            if key == start:
                break
        return path


def char_to_height(char):
    """
    Changes a character in the map to a
    more usable height value (integer)
    """
    if char == "S":
        return 0
    elif char == "E":
        return 25
    return ord(char) - 97


def run(data):
    grid_width = len(data[0].strip())
    grid_height = len(data)
    grid_size = grid_height * grid_width
    nodes = tuple(list(range(0, grid_size)))
    distances = {}

    for yidx, row in enumerate(data):
        for xidx, node in enumerate(row.strip()):
            node_id = (grid_width * yidx) + xidx
            distances[node_id] = {}
            height = char_to_height(node)

            if node == "S":
                # This is where we start...
                starting_node = node_id
            elif node == "E":
                # This is where we end...
                ending_node = node_id
            height = char_to_height(node)

            if yidx != 0:
                # up
                height_difference = (
                    char_to_height(data[yidx - 1].strip()[xidx]) - height
                )
                if height_difference > 1:
                    distances[node_id][(grid_width * (yidx - 1)) + xidx] = 1000000
                else:
                    distances[node_id][(grid_width * (yidx - 1)) + xidx] = 1
            if yidx + 1 != grid_height:
                # down
                height_difference = (
                    char_to_height(data[yidx + 1].strip()[xidx]) - height
                )
                if height_difference > 1:
                    distances[node_id][(grid_width * (yidx + 1)) + xidx] = 1000000
                else:
                    distances[node_id][(grid_width * (yidx + 1)) + xidx] = 1
            if xidx != 0:
                # left
                height_difference = char_to_height(row[xidx - 1]) - height
                if height_difference > 1:
                    distances[node_id][node_id - 1] = 1000000
                else:
                    distances[node_id][node_id - 1] = 1
            if (xidx + 1) % grid_width != 0:
                # right
                height_difference = char_to_height(row[xidx + 1]) - height
                if height_difference > 1:
                    distances[node_id][node_id + 1] = 1000000
                else:
                    distances[node_id][node_id + 1] = 1

    start_vertex = starting_node
    end_vertex = ending_node
    dijkstra = Dijkstra(nodes, distances)
    p, v = dijkstra.find_route(start_vertex, end_vertex)
    se = dijkstra.generate_path(p, start_vertex, end_vertex)
    return len(se) - 1


def run_p2(data):
    grid_width = len(data[0].strip())
    grid_height = len(data)
    grid_size = grid_height * grid_width
    nodes = tuple(list(range(0, grid_size)))
    distances = {}
    starting_points = []

    for yidx, row in enumerate(data):
        for xidx, node in enumerate(row.strip()):
            node_id = (grid_width * yidx) + xidx
            distances[node_id] = {}
            height = char_to_height(node)

            if node == "S" or node == "a":
                # This is where we can start...
                starting_points.append(node_id)
            elif node == "E":
                # This is where we end...
                ending_node = node_id
            height = char_to_height(node)

            if yidx != 0:
                # up
                height_difference = (
                    char_to_height(data[yidx - 1].strip()[xidx]) - height
                )
                if height_difference <= 1:
                    distances[node_id][(grid_width * (yidx - 1)) + xidx] = 1
            if yidx + 1 != grid_height:
                # down
                height_difference = (
                    char_to_height(data[yidx + 1].strip()[xidx]) - height
                )
                if height_difference <= 1:
                    distances[node_id][(grid_width * (yidx + 1)) + xidx] = 1
            if xidx != 0:
                # left
                height_difference = char_to_height(row[xidx - 1]) - height
                if height_difference <= 1:
                    distances[node_id][node_id - 1] = 1
            if (xidx + 1) % grid_width != 0:
                # right
                height_difference = char_to_height(row[xidx + 1]) - height
                if height_difference <= 1:
                    distances[node_id][node_id + 1] = 1

    shortest = None
    end_vertex = ending_node
    dijkstra = Dijkstra(nodes, distances)

    print("==============================")
    print("Starting Points Found: {}".format(len(starting_points)))
    print("==============================")
    for idx, starting_node in enumerate(starting_points):
        p, v = dijkstra.find_route(starting_node, end_vertex)
        se = dijkstra.generate_path(p, starting_node, end_vertex)
        if se == -1:
            continue
        print("Trying Starting Point {}: {}".format(idx, len(se) - 1))
        if shortest is None or len(se) - 1 < shortest:
            shortest = len(se) - 1
            print("--> A New Shortest Path!")
    return shortest
