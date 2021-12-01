import unittest
from pathlib import Path

import day01


class TestDay01(unittest.TestCase):

    def test_read_input(self):
        lines = day01.read_input(Path(day01.__file__).parent / "input_sample.txt")
        self.assertListEqual(lines[:5], [199, 200, 208, 210, 200])

    def test_find_changes(self):
        changes = day01.find_changes([199, 200, 208, 210, 200])
        self.assertListEqual(changes, [1, 8, 2, -10])

    def test_count_increases(self):
        increases = day01.count_increases([6, 3, 0, 4, -5, -99999999999999999999])
        self.assertListEqual(increases, [6, 3, 4])

    def test_sliding_window(self):
        lines = day01.read_input(Path(day01.__file__).parent / "input_sample.txt")
        sums = day01.sliding_sums(lines)
        self.assertListEqual(sums, [607, 618, 618, 617, 647, 716, 769, 792])


if __name__ == '__main__':
    unittest.main()
