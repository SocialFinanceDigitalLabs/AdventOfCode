import unittest
from pathlib import Path

import day04
from common import file_to_lines
from day04 import Board


class TestDay04(unittest.TestCase):

    def test_line_to_numbers(self):
        self.assertListEqual(day04._line_to_int_array("1,2,3,4,5,6", sep=","), [1, 2, 3, 4, 5, 6])
        self.assertListEqual(day04._line_to_int_array("1 2   3 4 5 6 "), [1, 2, 3, 4, 5, 6])

    def test_read_input(self):
        sample_input = """
1,5,30,4,6

 1  2  3
22 23 24
 4 25  6

5 6 7 
6 5 5
7 6 6""".splitlines()
        numbers, boards = day04.parse_input(sample_input)
        self.assertListEqual(numbers, [1, 5, 30, 4, 6])
        self.assertEqual(len(boards), 2)

    def test_board(self):
        board = Board(["1 2 3 ", " 2 3 4", "4 5 6"])
        self.assertEqual(board.sum, 30)
        self.assertListEqual(board.rows[0].tolist(), [1, 2, 3])
        self.assertListEqual(board.columns[0].tolist(), [1, 2, 4])

    def test_bingo(self):
        board = Board(["1 2 3 ", " 2 3 4", "4 5 6"])
        self.assertIsNotNone(board.bingo([2, 3, 5]))
        self.assertIsNotNone(board.bingo([3, 4, 6]))
        self.assertIsNone(board.bingo([1, 2, 5, 9, 10, 21]))
        self.assertIsNotNone(board.bingo([10, 5, 34, 21, 3, 6, 2]))

    def test_sum_unmarked(self):
        board = Board(["1 2 3", "4 5 6", "7 8 9"])
        self.assertEqual(board.sum_unmarked([]), 45)
        self.assertEqual(board.sum_unmarked([1]), 44)
        self.assertEqual(board.sum_unmarked([1, 4, 5, 10, 25]), 35)
