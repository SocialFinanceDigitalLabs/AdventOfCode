# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:37:42 2020

@author: celine.gross
"""

import itertools

with open('input_day9.txt', 'r') as file:
    puzzle = [int(x.strip()) for x in file]


# Part 1

def find_invalid_number(data, preamble=25):
    for i, number in enumerate(data[preamble:]):
        preamble_numbers = set(data[i:i+preamble])
        sums = [sum(combination) for combination in itertools.combinations(preamble_numbers, 2)]
        if number not in sums:
            return number
    return 'No invalid number found'

print(find_invalid_number(puzzle))


# Part 2

def find_encryption_weakness(data):
    invalid_number = find_invalid_number(data)
    for i, number in enumerate(data):
        contiguous = []
        j = int(i)
        while sum(contiguous) < invalid_number:
            contiguous.append(data[j])
            j += 1
        if sum(contiguous) == invalid_number:
            return min(contiguous) + max(contiguous)
    return 'No encryption weakness found'

print(find_encryption_weakness(puzzle))