# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:04:59 2020

@author: celine.gross
"""

import numpy as np

with open('input_day11.txt', 'r') as file:
    puzzle = [[x for x in line.strip()] for line in file]
    puzzle = np.array(puzzle)


# Part 1

def count_seats_taken(data):
    count = 0
    for row in data:
        for seat in row:
            if seat == '#':
                count+=1
    return count


def seat_to_free(x, y, data):
    if data[x][y] != '#':
        return False
    else:
        count = 0
        for row in data[max(0, x-1): min(x+1, len(data)-1)+1]:
            for seat in row[max(0, y-1): min(y+1, len(data[0])-1)+1]:
                if seat == '#':
                    count += 1
        if count>4:
            return True
    return False


def seat_to_take(x, y, data):
    if data[x][y] != 'L':
        return False
    else:
        for i in range(max(0, x-1), min(x+1, len(data)-1)+1):
            for j in range(max(0, y-1), min(y+1, len(data[0])-1)+1):
                if data[i][j] == '#':
                    return False
    return True


def get_seat_coordinates(data):
    to_free = set()
    to_take = set()
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if seat_to_free(i, j, data):
                to_free.add((i,j))
            elif seat_to_take(i, j, data):
                to_take.add((i,j))         
    return to_free, to_take


def update_seats(data, to_free, to_take):
    for x,y in to_free:
        data[x][y] = 'L'
    for x,y in to_take:
        data[x][y] = '#'
    return data


def run(data):
    changes = True
    while changes:
        to_free, to_take = get_seat_coordinates(data)
        data = update_seats(data, to_free, to_take)
        if (len(to_free) == 0 and len(to_take) == 0):
            changes = False        
    return count_seats_taken(data)


print(run(puzzle))
    

# Part 2

def count_visible_seats(x, y, data):
    count = 0
    directions = [(1,0), (-1,0), (0,1), (0, -1), (1,1), (-1,-1), (1,-1), (-1,1)]
    for direction in directions:
        i, j = x, y
        while True: 
            i, j = i+direction[0], j+direction[1]
            if (0 <= i < len(data)) and (0 <= j < len(data[0])):
                if data[i][j] == '#':
                    count += 1
                    break
                elif data[i][j] == 'L':
                    break
            else:
                break
    return count


def seat_to_free(x, y, data):
    if data[x][y] != '#':
        return False
    else:
        if count_visible_seats(x, y, data) >= 5:
            return True
    return False


def seat_to_take(x, y, data):
    if data[x][y] != 'L':
        return False
    else:
       if count_visible_seats(x, y, data) ==0:
           return True
    return False


def get_seat_coordinates(data):
    to_free = set()
    to_take = set()
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if seat_to_free(i, j, data):
                to_free.add((i,j))
            elif seat_to_take(i, j, data):
                to_take.add((i,j))         
    return to_free, to_take


def run(data):
    changes = True
    while changes:
        to_free, to_take = get_seat_coordinates(data)
        data = update_seats(data, to_free, to_take)
        if (len(to_free) == 0 and len(to_take) == 0):
            changes = False        
    return count_seats_taken(data)


print(run(puzzle))

    