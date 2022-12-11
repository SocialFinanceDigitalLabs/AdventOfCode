# Advent of Code 2021 Day 22
import unittest

import day22
from day22.database import Database


class TestDay22(unittest.TestCase):

    def test_split_coords(self):
        self.assertEqual((-20, 26), day22.split_coords('x', 'x=-20..26'))

    def test_parse_input(self):
        self.assertEqual((
            (10, 12),
            (10, 12),
            (10, 12),
            1
        ), day22.parse_input('on x=10..12,y=10..12,z=10..12'))

    def test_limit(self):
        self.assertEqual((-50, 0), day22.limit(-50 , 0, -50, 50))
        self.assertEqual((-50, 0), day22.limit(-100 , 0, -50, 50))
        self.assertEqual((-50, -50), day22.limit(-100 , -50, -50, 50))
        self.assertEqual(None, day22.limit(-100 , -51, -50, 50))

    def test_set_single(self):
        with Database.open() as db:
            db.set_value(1,1,1,1)
            self.assertEqual(1, db.count_values(1))

    def test_set_many(self):
        with Database.open() as db:
            db.set_many((-50, 50), (-50, 50), (-50, 50), 1)
            self.assertEqual(101**3, db.count_values(1))

    def test_box_intersect(self):
        b1 = day22.Box(0, 10, 0, 10, 0, 10)
        b2 = day22.Box(5, 15, 5, 15, 5, 15)

        self.assertTrue(b1.intersects(b2))
        self.assertEqual(day22.Box(5, 10, 5, 10, 5, 10), b1.intersect(b2))

        b3 = day22.Box(15, 20, 15, 20, 15, 20)
        self.assertFalse(b1.intersects(b3))

        with self.assertRaises(ValueError):
            self.assertEqual(None, b1.intersect(b3))

