from aocd import get_data
from functools import reduce

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

tree_formation = get_data(day=8, year=2022, session=session)
tree_rows = tree_formation.splitlines()


def pivot_forest(tree_rows):
    tree_columns = []
    ix = 0
    for row in tree_rows:
        tree_column = ""
        for x in tree_rows:
            tree_column += x[ix]
        tree_columns.append(tree_column)
        ix += 1
    return tree_columns


tree_columns = pivot_forest(tree_rows)


def conv_reverse_x(x_value):
    return 98-x_value


def find_visible(tree_formation, direction, visible):
    y = -1
    for row in tree_formation:
        y += 1
        x = -1
        if direction == "right" or direction == "down":
            row = row
        if direction == "left" or direction == "up":
            row = row[::-1]
        for tree in row:
            tree = int(tree)
            x += 1
            int_row = [int(value) for value in str(row[x:])]
            if all(tree > i for i in int_row[1:]):
                if direction == "right":
                    visible[x, y] = tree
                if direction == "left":
                    visible[conv_reverse_x(x), y] = tree
                if direction == "down":
                    visible[y, x] = tree
                if direction == "up":
                    visible[y, conv_reverse_x(x)] = tree
            if len(int_row) == 1:
                if direction == "right":
                    visible[x, y] = tree
                if direction == "left":
                    visible[conv_reverse_x(x), y] = tree
                if direction == "down":
                    visible[y, x] = tree
                if direction == "up":
                    visible[y, conv_reverse_x(x)] = tree
    return visible


visible = {}

find_visible(tree_rows, "right", visible)
find_visible(tree_rows, "left", visible)
find_visible(tree_columns, "up", visible)
find_visible(tree_columns, "down", visible)

print(len(visible))


def number_of_visible_trees(tree, row_of_trees):
    number_of_trees = 0
    if len(row_of_trees) == 1:
        return number_of_trees
    for current_tree in row_of_trees[1:]:
        if tree > current_tree:
            number_of_trees += 1
        elif tree <= current_tree:
            number_of_trees += 1
            return number_of_trees
    return number_of_trees


def calculate_view_distance(tree_formation, direction, scenic_score):
    y = -1
    for row in tree_formation:
        y += 1
        x = -1
        if direction == "right" or direction == "down":
            row = row
        if direction == "left" or direction == "up":
            row = row[::-1]
        for tree in row:
            tree = int(tree)
            x += 1
            int_row = [int(value) for value in str(row[x:])]
            if direction == "right":
                scenic_score[x, y].append(number_of_visible_trees(tree, int_row))
            if direction == "left":
                scenic_score[conv_reverse_x(x), y].append(number_of_visible_trees(tree, int_row))
            if direction == "down":
                scenic_score[y, x].append(number_of_visible_trees(tree, int_row))
            if direction == "up":
                scenic_score[y, conv_reverse_x(x)].append(number_of_visible_trees(tree, int_row))
    return scenic_score


def calculate_scenic_score(list):
    scenic_score = reduce(lambda x, y: x*y, list)
    return scenic_score


scenic_scores = {}

for x in range(99):
    for y in range(99):
        scenic_scores[x, y] = []

calculate_view_distance(tree_rows, "right", scenic_scores)
calculate_view_distance(tree_rows, "left", scenic_scores)
calculate_view_distance(tree_columns, "up", scenic_scores)
calculate_view_distance(tree_columns, "down", scenic_scores)

highest_score = 0
for value in scenic_scores.values():
    scenic_score = calculate_scenic_score(value)
    highest_score = scenic_score if scenic_score > highest_score else highest_score

print(highest_score)

