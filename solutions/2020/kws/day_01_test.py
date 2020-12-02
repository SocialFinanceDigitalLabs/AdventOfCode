import unittest
from day_01 import find_target, find_three_target
from kws.aoc2020 import split_input

SAMPLE = """
1721
979
366
299
675
1456
"""


class AdventOfCode01TestCase(unittest.TestCase):

    def test_find_matches(self):
        values = split_input(SAMPLE, type=int)

        v1, v2 = find_target(values)

        self.assertEqual(v1 + v2, 2020)
        self.assertEqual(v1, 299)
        self.assertEqual(v2, 1721)

    def test_find_three_matches(self):
        values = split_input(SAMPLE, type=int)

        v1, v2, v3 = find_three_target(values)

        self.assertEqual(v1 + v2 + v3, 2020)
        self.assertEqual(v1, 366)
        self.assertEqual(v2, 979)
        self.assertEqual(v3, 675)



if __name__ == '__main__':
    unittest.main()
