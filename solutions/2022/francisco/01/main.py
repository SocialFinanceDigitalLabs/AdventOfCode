from util import FileParser as BaseFileParser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class FileParser(BaseFileParser):
    def load(self):
        with open(self.file_path) as file:
            data = [
                [int(elf_food) for elf_food in elf_data.split("\n")]
                for elf_data in file.read().split("\n\n")
            ]
        return data


def part_1(file: str):
    parser = FileParser(dir_path, file)
    data = parser.read()
    max_calories = 0
    for food in data:
        calories = sum(food)
        if calories > max_calories:
            max_calories = calories
    return max_calories


def part_2(file):
    parser = FileParser(dir_path, file)
    data = parser.read()
    all_calories = []
    for food in data:
        all_calories.append(sum(food))
    
    all_calories.sort()
    return(sum(all_calories[-3:]))