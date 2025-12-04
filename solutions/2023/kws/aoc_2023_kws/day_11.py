import click
import numpy as np
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit
from scipy.spatial.distance import pdist


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day11(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day11.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day11.txt").read_text()

    input_data = input_data.splitlines()
    input_data = [list(line) for line in input_data]
    orig_data = np.array(input_data)
    input_data = orig_data.copy()

    # Find the rows that only contain "." entries
    rows_with_only_dots = np.all(input_data == ".", axis=1)
    indices_of_rows_with_only_dots = np.where(rows_with_only_dots)[0]

    # Find the columns that only contain "." entries
    cols_with_only_dots = np.all(input_data == ".", axis=0)
    indices_of_cols_with_only_dots = np.where(cols_with_only_dots)[0]

    # Insert a column of "."s before each row
    input_data = np.insert(input_data, indices_of_rows_with_only_dots, "x", axis=0)

    # Insert a column of "."s before each column
    input_data = np.insert(input_data, indices_of_cols_with_only_dots, "y", axis=1)

    # Find the x, y coordinates of each '#'
    coordinates = np.argwhere(input_data == "#")

    # Calculate pairwise distances between coordinates
    pairwise_distances = pdist(coordinates, metric="cityblock")

    # Print the pairwise distances
    print(pairwise_distances)
    print(len(pairwise_distances))
    print(sum(pairwise_distances))

    test = [[0, 4], [11, 9]]
    print(pdist(test, metric="cityblock"))

    part2_data = orig_data.copy()
    coordinates = np.argwhere(part2_data == "#")

    scale = 1_000_000
    # scale = 100

    scale -= 1

    print("Adjusted coordinates")
    adjusted_coordinates = []
    for x, y in coordinates:
        cols = sum([1 for i in indices_of_cols_with_only_dots if i < y]) * scale
        rows = sum([1 for i in indices_of_rows_with_only_dots if i < x]) * scale
        if cols:
            y += cols
        if rows:
            x += rows
        print(x, y, cols, rows)
        adjusted_coordinates.append([x, y])

    pairwise_distances = pdist(adjusted_coordinates, metric="cityblock")
    print(sum(pairwise_distances))
