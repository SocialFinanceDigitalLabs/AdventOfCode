import numpy as np


def _line_to_int_array(line, sep=" "):
    return [int(v) for v in line.split(sep) if v.strip() != ""]


class Board:

    def __init__(self, lines):
        lines = [_line_to_int_array(l) for l in lines]
        self.rows = np.array(lines, dtype=int)
        self.columns = self.rows.T
        self.all_values = self.rows.flatten()

    @property
    def sum(self):
        return self.rows.sum()

    def bingo(self, values):
        target = self.rows.shape[0]
        for row in self.rows:
            if len(np.intersect1d(row, values)) == target:
                return row
        for col in self.columns:
            if len(np.intersect1d(col, values)) == target:
                return col
        return None

    def sum_unmarked(self, values):
        return self.sum - np.intersect1d(values, self.all_values).sum()


def parse_input(value):
    value += [""]  # Just to make sure we always flush the last value

    ix = 0
    first_row = []
    for ix, row in enumerate(value):
        if row.strip() != "":
            first_row = _line_to_int_array(row, sep=",")
            break

    boards = []
    current_lines = []
    for row in value[ix+1:]:
        if len(row.strip()) == 0:
            if len(current_lines) > 0:
                boards.append(Board(current_lines))
            current_lines = []
            continue
        current_lines.append(row)

    return first_row, boards

