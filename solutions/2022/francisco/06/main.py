from util import FileParser as BaseFileParser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class FileParser(BaseFileParser):
    def load(self) -> list:
        with open(self.file_path) as f:
            data = f.read()
        return data

def part_1(file: str):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    data = parser.read()
    for idx in range(len(data)):
        subset = data[idx:idx+4]
        if len(subset) == len(set(subset)):
            return idx + 4


        


def part_2(file):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    data = parser.read()
    for idx in range(len(data)):
        subset = data[idx:idx+14]
        if len(subset) == len(set(subset)):
            return idx + 14

