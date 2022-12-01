# Advent of Code 2021 Day 5
import unittest
import day05


class TestDay05(unittest.TestCase):

    def test_parse_input(self):
        vents = day05.parse_input(["1,1 -> 1,2", "2,1 -> 2,2", "1,2 -> 1,3"])
        vents = list(vents)
        self.assertEqual(len(vents), 3)
        self.assertEqual(vents[0].start, (1, 1))
        self.assertEqual(vents[0].end, (1, 2))

    def test_vent_map(self):
        vent = day05.Vent.from_string("1,1 -> 1,2")
        self.assertEqual(vent.dimension, 3)
        self.assertListEqual(vent.map.tolist(), [[0, 0, 0], [0, 1, 0], [0, 1, 0]])

        vent = day05.Vent.from_string("0,0 -> 3,0")
        self.assertEqual(vent.dimension, 4)
        self.assertListEqual(vent.map.tolist(), [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        vent = day05.Vent.from_string("3,0 -> 0,0")
        self.assertEqual(vent.dimension, 4)
        self.assertListEqual(vent.map.tolist(), [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        vent = day05.Vent.from_string("0,0 -> 3,3")
        self.assertEqual(vent.dimension, 4)
        self.assertListEqual(vent.map.tolist(), [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        vent = day05.Vent.from_string("3,0 -> 0,3")
        self.assertEqual(vent.dimension, 4)
        self.assertListEqual(vent.map.tolist(), [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])


    def test_intersects(self):
        vent1 = day05.Vent.from_string("1,1 -> 1,2")
        vent2 = day05.Vent.from_string("0,1 -> 2,1")

        result = day05.Vent.add(vent1, vent2)
        self.assertListEqual(result.tolist(), [[0, 0, 0], [1, 2, 1], [0, 1, 0]])
