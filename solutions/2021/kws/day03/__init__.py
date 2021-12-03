import math
from typing import Iterable, List

import numpy as np


def most_common_value(values: Iterable[Iterable[int]], keep: int) -> List[int]:
    array = np.array(values, np.int32)
    means = np.mean(array, axis=0)
    most_common = [v * 2 for v in means]
    if keep == 1:
        return [1 if v >= 1 else 0 for v in most_common]
    else:
        return [0 if v <= 1 else 1 for v in most_common]


def input_to_array(values: Iterable[str]) -> List[List[int]]:
    return [[int(i) for i in line if i.isdigit()] for line in values]


def list_to_binary(values: Iterable[int]) -> str:
    return "".join([str(v) for v in values])


def invert(values: Iterable[int]):
    """ We could do unsigned binary unary here - but I prefer to be able to visualise the result """
    return [0 if v else 1 for v in values]


def filter(subset: Iterable[Iterable[int]], subset_values: List[int]) -> List[Iterable[int]]:
    comp_length = len(subset_values)
    return [line for line in subset if line[:comp_length] == subset_values]


def generator_rating(values: Iterable[Iterable[int]], inverted: bool) -> List[int]:
    bits = len(values[0])

    most_common = most_common_value(values, keep=1)
    subset_filter = []
    subset_values = values
    for b in range(bits):
        if inverted:
            most_common = invert(most_common)
        subset_filter.append(most_common[b])
        subset_values = filter(subset_values, subset_filter)
        if len(subset_values) == 1:
            return subset_values[0]
        most_common = most_common_value(subset_values, keep=1)

    return most_common
