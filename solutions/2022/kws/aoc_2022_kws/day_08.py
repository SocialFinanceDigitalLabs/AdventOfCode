from collections import namedtuple
from typing import Iterable

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich.progress import track

Tree = namedtuple("Tree", "x,y,height")
ScenicScore = namedtuple("ScenicScore", "x,y,score")


def parse_trees(input_data):
    for y, line in enumerate(input_data.splitlines()):
        for x, char in enumerate(line):
            if char.isdigit():
                yield Tree(x, y, int(char))


def find_visible(tree_list: Iterable[Tree]):
    highest = -1
    for tree in tree_list:
        if tree.height > highest:
            highest = tree.height
            yield tree


def find_visible_top(tree, tree_list: Iterable[Tree]):
    for t in tree_list:
        yield t
        if t.height >= tree.height:
            return


def get_scenic_score(tree, row, col):
    left = [t for t in row if t.x < tree.x][::-1]
    right = [t for t in row if t.x > tree.x]
    up = [t for t in col if t.y < tree.y][::-1]
    down = [t for t in col if t.y > tree.y]

    visible_left = list(find_visible_top(tree, left))
    visible_right = list(find_visible_top(tree, right))
    visible_up = list(find_visible_top(tree, up))
    visible_down = list(find_visible_top(tree, down))

    score = ScenicScore(
        tree.x,
        tree.y,
        len(visible_left) * len(visible_right) * len(visible_up) * len(visible_down),
    )

    return score


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day08(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day08.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day08.txt").read_text()
    trees = list(parse_trees(input_data))

    row_count = max(t.y for t in trees) + 1
    col_count = max(t.x for t in trees) + 1

    visible_trees = set()

    # Visible rows
    for y in range(row_count):
        tree_list = [t for t in trees if t.y == y]
        tree_list.sort(key=lambda t: t.x)
        visible_trees.update(set(find_visible(tree_list)))
        tree_list.sort(key=lambda t: t.x, reverse=True)
        visible_trees.update(set(find_visible(tree_list)))

    # Visible columns
    for x in range(col_count):
        tree_list = [t for t in trees if t.x == x]
        tree_list.sort(key=lambda t: t.y)
        visible_trees.update(set(find_visible(tree_list)))
        tree_list.sort(key=lambda t: t.y, reverse=True)
        visible_trees.update(set(find_visible(tree_list)))

    print("Part 1 - Visible trees:", len(visible_trees))

    # Part 2
    scenic_scores = []
    for tree in track(trees):
        row = [t for t in trees if t.y == tree.y]
        col = [t for t in trees if t.x == tree.x]
        scenic_scores.append(get_scenic_score(tree, row, col))

    best_score = max(scenic_scores, key=lambda s: s.score)
    print("Part 2 - Best scenic score:", best_score)


if __name__ == "__main__":
    day08(["--sample"])
