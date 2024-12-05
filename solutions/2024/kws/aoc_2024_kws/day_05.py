"""
Day 5: Book Ordering

This is a bit of a mess. Part 1 was relatively easy, but part 2 requires re-ordering the pages based on evaluating the "before" and "after" rules. I first tried to create a directed graph,
and this worked fine for the sample input, but not for the actual input. There were loads of cycles, and breaking on a cycle or removing edges did not seem to work.

The real data is too big to try a naive random search, so I tried a greedy approach, which worked. Not the nicest solution, but it got me there. Messy code below.


"""
import math
import click
from aocd import submit as aocd_submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config

pages = {}

class Page:
    def __init__(self, id: int):
        self.id = id
        self.before = []
        self.after = []

    @staticmethod
    def get(id: int):
        if id not in pages:
            pages[id] = Page(id)
        return pages[id]
    
    def __repr__(self):
        return f"Page {self.id}"
    
def find_valid_ordering(pages: list[Page]) -> list[Page]:
    """
    Greedily orders pages by selecting the best candidate at each position.
    A page is a better candidate if:
    1. It satisfies more of its "before" rules (most of its before pages are already placed)
    2. It has more "after" rules to satisfy (more pages should come after it)
    """
    remaining = set(pages)
    result = []
    
    def score_candidate(page: Page) -> tuple[int, int]:
        before_satisfied = sum(1 for p in page.before if p in result)
        before_total = len(page.before)
        after_potential = sum(1 for p in page.after if p in remaining)
        return (before_satisfied / (before_total + 1), after_potential)
    
    while remaining:
        best_page = max(remaining, key=score_candidate)
        result.append(best_page)
        remaining.remove(best_page)
    
    return result


def find_valid_ordering(pages: list[Page]) -> list[Page]:
    """
    Greedily orders pages by selecting the best candidate at each position.
    A page is a better candidate if:
    1. It satisfies more of its "before" rules (most of its before pages are already placed)
    2. It has more "after" rules to satisfy (more pages should come after it)
    """
    remaining = set(pages)
    result = []
    
    def score_candidate(page: Page) -> tuple[int, int]:
        before_satisfied = sum(1 for p in page.before if p in result)
        before_total = len(page.before)
        after_potential = sum(1 for p in page.after if p in remaining)
        # Prioritize pages that have most of their "before" rules satisfied
        # and have the most "after" rules yet to be satisfied
        return (before_satisfied / (before_total + 1), after_potential)
    
    while remaining:
        # Select the best candidate based on our scoring function
        best_page = max(remaining, key=score_candidate)
        result.append(best_page)
        remaining.remove(best_page)
    
    return result



def sort_pages(pages):
    """
    Tried to create a directed graph, but this approach did not seem to work....
    """
    pages = {p.id: p for p in pages}
    graph = {} 

    for page_id in pages:
        graph[page_id] = set()
    
    for page_id, page in pages.items():
        for before_page in page.before:
            graph.setdefault(before_page.id, set()).add(page_id)
        for after_page in page.after:
            graph[page_id].add(after_page.id)

    visited = {}  # 0 = unvisited, 1 = in current path, 2 = completely visited
    result = []
    cycle_edges = set()  # Store edges that create cycles

    def dfs(node_id, path=None):
        if path is None:
            path = set()
            
        if node_id in path:  # Cycle detected
            # Find the edge that created the cycle
            path_list = list(path)
            cycle_start = path_list.index(node_id)
            cycle = path_list[cycle_start:]
            # Add all edges in the cycle to cycle_edges
            for i in range(len(cycle)):
                cycle_edges.add((cycle[i], cycle[(i + 1) % len(cycle)]))
            return
            
        if visited.get(node_id, 0) == 2:
            return

        visited[node_id] = 1
        path.add(node_id)
        
        for neighbor_id in graph.get(node_id, []):
            if (node_id, neighbor_id) not in cycle_edges:  # Skip cycle edges
                dfs(neighbor_id, path)
                
        path.remove(node_id)
        visited[node_id] = 2
        result.append(node_id)

    for node_id in graph:
        if visited.get(node_id, 0) == 0:
            dfs(node_id)

    sorted_page_ids = result[::-1]
    sorted_pages = [pages.get(pid) for pid in sorted_page_ids]
    return [x for x in sorted_pages if x is not None]



def evaluate_sequence(sequence: list[Page]):
    """
    Checks that for each page in the sequence, make sure that all the pages before it are in the "before" list, and that all the pages after it are in the "after" list.
    """
    for i, page in enumerate(sequence):
        if not all(before in page.before for before in sequence[:i]):
            return False
        if not all(after in page.after for after in sequence[i+1:]):
            return False
    return True

             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--submit", "-S", is_flag=True)
def day05(sample, submit):
    if sample:
        input_data = (config.SAMPLE_DIR / "day05.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day05.txt").read_text()
    
    input_data = input_data.strip()
    input_data = [x.strip() for x in input_data.splitlines()]
    
    separator = input_data.index("")
    ordering, changes = input_data[:separator], input_data[separator+1:]

    for line in ordering:
        before, after = line.split("|", 1)
        before_page = Page.get(int(before))
        after_page = Page.get(int(after))
        before_page.after.append(after_page)
        after_page.before.append(before_page)


    sequences = []
    for line in changes:
        if not line:
            break
        page_sequence = [Page.get(int(page)) for page in line.split(",")]

        is_valid = evaluate_sequence(page_sequence)
        sequences.append((is_valid, page_sequence))

    valid_sequences = [sequence[1] for sequence in sequences if sequence[0]]

    middle_pages = [sequence[len(sequence)//2].id for sequence in valid_sequences]
    my_answer = sum(middle_pages)
    print(my_answer)
    if submit:
        aocd_submit(my_answer, part="a", day=5, year=2024)

    invalid_sequences = [sequence[1] for sequence in sequences if not sequence[0]]
    reordered_sequences = [find_valid_ordering(sequence) for sequence in invalid_sequences]
    for s in reordered_sequences:
        print(s)

    middle_pages = [sequence[len(sequence)//2] for sequence in reordered_sequences]
    my_answer_part2 = sum([m.id for m in middle_pages])
    print(my_answer_part2)
    if submit:
        aocd_submit(my_answer_part2, part="b", day=5, year=2024)

    # middle_pages_part2 = [sequence[len(sequence)//2].id for sequence in reordered_sequences]
    # my_answer_part2 = sum(middle_pages_part2)
    # print(my_answer_part2)
    # if submit:
    #     aocd_submit(my_answer_part2, part="b", day=5, year=2024)


