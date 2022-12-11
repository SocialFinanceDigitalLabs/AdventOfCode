from util import FileParser
import os
import math
from dataclasses import dataclass
import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Tree:
    id: int
    row: int
    col: int
    height: int

    @classmethod
    def parse(cls, height: int, id: int, row_count: int, col_count: int):
        row = math.floor(id / col_count)
        col = id % row_count
        return cls(row=row, col=col, height=height, id=id)


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    row_count = len(data)
    col_count = len(data[0])
    data = [int(d) for row in data for d in row]
    print(data)
    trees: list[Tree] = []
    for id, height in enumerate(data):
        trees.append(
            Tree.parse(height=height, id=id, row_count=row_count, col_count=col_count)
        )

    visible_count = 0
    for tree in tqdm.tqdm(trees):
        if (
            tree.col == 0
            or tree.row == 0
            or tree.col == col_count - 1
            or tree.row == row_count - 1
        ):
            visible_count += 1
            continue
        col_trees_before = [
            other_tree
            for other_tree in trees
            if other_tree.col == tree.col
            and other_tree.row < tree.row
            and other_tree.height >= tree.height
        ]
        col_trees_after = [
            other_tree
            for other_tree in trees
            if other_tree.col == tree.col
            and other_tree.row > tree.row
            and other_tree.height >= tree.height
        ]
        row_trees_before = [
            other_tree
            for other_tree in trees
            if other_tree.row == tree.row
            and other_tree.col < tree.col
            and other_tree.height >= tree.height
        ]
        row_trees_after = [
            other_tree
            for other_tree in trees
            if other_tree.row == tree.row
            and other_tree.col > tree.col
            and other_tree.height >= tree.height
        ]
        if (
            not col_trees_before
            or not col_trees_after
            or not row_trees_before
            or not row_trees_after
        ):
            visible_count += 1
    return visible_count


def get_tree_score(trees: list[Tree], tree: Tree) -> int:
    score = 0
    for other_tree in trees:
        score += 1
        if other_tree.height >= tree.height:
            break
    return score


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    row_count = len(data)
    col_count = len(data[0])
    data = [int(d) for row in data for d in row]
    trees: list[Tree] = []
    for id, height in enumerate(data):
        trees.append(
            Tree.parse(height=height, id=id, row_count=row_count, col_count=col_count)
        )

    max_tree_score = 0
    for tree in tqdm.tqdm(trees):
        col_trees = [other_tree for other_tree in trees if other_tree.col == tree.col]
        row_trees = [other_tree for other_tree in trees if other_tree.row == tree.row]
        col_trees_before = [
            other_tree for other_tree in col_trees if other_tree.row < tree.row
        ]
        col_trees_after = [
            other_tree for other_tree in col_trees if other_tree.row > tree.row
        ]

        row_trees_before = [
            other_tree for other_tree in row_trees if other_tree.col < tree.col
        ]
        row_trees_after = [
            other_tree for other_tree in row_trees if other_tree.col > tree.col
        ]

        tree_score =(
            get_tree_score(col_trees_before[::-1], tree)
            * get_tree_score(col_trees_after, tree)
            * get_tree_score(row_trees_before[::-1], tree)
            * get_tree_score(row_trees_after, tree)
        )
        if tree_score > max_tree_score:
            max_tree_score = tree_score
    return max_tree_score
