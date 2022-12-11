from util import FileParser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def part_1(file: str):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    data = parser.read()
    count = 0
    for group in data:
        elf1, elf2 = [list(map(int, elf.split('-'))) for elf in group.split(',')]
        elf1_range = list(range(elf1[0], elf1[-1] + 1))
        elf2_range = list(range(elf2[0], elf2[-1] + 1))
        if set(elf1_range) <= set(elf2_range) or set(elf2_range) <= set(elf1_range):
            print(elf1_range)
            print(elf2_range)
            print("\n")
            count += 1
    return count

def part_2(file):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    data = parser.read()
    count = 0
    for group in data:
        elf1, elf2 = [list(map(int, elf.split('-'))) for elf in group.split(',')]
        elf1_range = list(range(elf1[0], elf1[-1] + 1))
        elf2_range = list(range(elf2[0], elf2[-1] + 1))

        if any([section for section in elf1_range if section in elf2_range]):
            count += 1
    return count

