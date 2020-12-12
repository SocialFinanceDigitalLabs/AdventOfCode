# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:49:27 2020

@author: celine.gross
"""

from collections import Counter

with open('input_day10.txt', 'r') as file:
    puzzle = [int(x.strip()) for x in file]

print(puzzle[:10])

# Part 1

def count_jolt_differences(data, start=0, end=+3):
    data.extend([start, max(data)+int(end)])
    data.sort()
    jolt_differences = [data[i+1] - data[i] for i, number in enumerate(data[:-1])]
    return Counter(jolt_differences)

def run(data):
    counts = count_jolt_differences(data)
    return counts[1]*counts[3]
    
print(run(puzzle))


# Part 2

print(len(puzzle))