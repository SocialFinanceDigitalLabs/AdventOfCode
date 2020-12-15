# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 10:57:56 2020

@author: celine.gross
"""

puzzle = [15,5,1,4,7,0]

def nth_number(data, n):
    # Store initial numbers read aloud
    numbers = {d:[i+1] for i, d in enumerate(data)}
    last = data[-1]
    # Start deducing new numbers until nth
    for i in range(len(data)+1, n+1):
        # Determine new number spoken, which becomes "last"
        if len(numbers[last]) == 1:
            last = 0
        else:
            last = numbers[last][-1] - numbers[last][-2]
        # Store new number in dict with the turn number
        if last in numbers:
            numbers[last].append(i)
        else:
            numbers[last] = [i]
    return last


print(nth_number(puzzle, 2020))    