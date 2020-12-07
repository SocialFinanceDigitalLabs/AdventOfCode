# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:07:47 2020

@author: celine.gross
"""

with open('input_day6.txt', 'r') as file:
    puzzle = file.read().strip().split('\n\n')
    puzzle = [line.split('\n') for line in puzzle]
    

# Part 1

def count_any_yes(group):
    group_answers = ''.join(group)
    unique_answers= set([letter for letter in group_answers])
    return len(unique_answers)

def run(data):
    return sum(count_any_yes(item) for item in data)

print(run(puzzle))


# Part 2

def count_all_yes(group):
    return len(set(group[0]).intersection(*group[1:]))

def run2(data):
    return sum(count_all_yes(item) for item in data)

print(run2(puzzle))