# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:24:50 2020

@author: celine.gross
"""
import re

with open('input_day7.txt', 'r') as file:
    puzzle = file.read().strip().split('\n')


# Part 1
    
# Clean puzzle input

def clean_bag_rules(bags):
    clean_bags = {}
    for bag in bags:
        parent, bigchild = bag.split(' bags contain ')
        assert parent not in clean_bags
        children = bigchild.split(', ')
        clean_children = {}
        for child in children:
            match = re.search('(\d+)\s(\w+\s\w+)\sbags?.?', child)
            if match is None:
                clean_bags[parent] = None
            else:
                clean_children[match.group(2)] = match.group(1)   
                clean_bags[parent] = clean_children
    return clean_bags

puzzle = clean_bag_rules(puzzle)


# Count bags leading eventually to shiny gold

def contains_color(bag_color, bags, color='shiny gold'):  
    child_colors = bags[bag_color]
    if child_colors is not None:
        # Base case
        if color in child_colors.keys():
            return True
        # Recursive case 
        for item in child_colors.keys():
            if contains_color(item, bags, color):
                return True
    return False

print(sum([contains_color(bag, puzzle) for bag in puzzle]))


# Part 2

def count_bags(bags, color='shiny gold'):
    children = bags[color]
    # Base case
    if children is None:
        return 1
    # Recursive case
    total = 1
    for child in children:
        total += int(children[child])*count_bags(bags, color=child)
    return total

print(count_bags(puzzle)-1) # Not counting initial shiny gold bag
