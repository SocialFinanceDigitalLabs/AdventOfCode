from util import FileParser
import os
import string

dir_path = os.path.dirname(os.path.realpath(__file__))
priorities = string.ascii_lowercase + string.ascii_uppercase

def part_1(file: str):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    data = parser.read()
    print(data)
    
    result = 0
    for rucksack in data:
        middle = int(len(rucksack)/2)
        item1 = rucksack[:middle]
        item2 = rucksack[middle:]
        common_char = [i for i in item1 if i in item2][0]
        result += priorities.index(common_char) + 1

    return result

def part_2(file):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    data = parser.read()

    result = 0
    for group in zip(*[iter(data)]*3):
        for i in group[0]:
            if i in group[1] and i in group [2]:
                result += priorities.index(i) + 1
                break

    return result
