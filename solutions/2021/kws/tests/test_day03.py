import unittest
import day03


class TestDay03(unittest.TestCase):

    def test_input_to_array(self):
        values = [
            "11",
            "10",
            "01",
            "00",
        ]
        self.assertListEqual(day03.input_to_array(values), [
            [1, 1],
            [1, 0],
            [0, 1],
            [0, 0],
        ])

    def test_most_common(self):
        values = [
            [1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ]
        result = day03.most_common_value(values, keep=0)
        self.assertListEqual(result, [1, 1, 0, 0, 0])

        result = day03.most_common_value(values, keep=1)
        self.assertListEqual(result, [1, 1, 1, 0, 0])

    def test_list_to_binary(self):
        self.assertEqual(day03.list_to_binary([1, 0, 0, 1]), "1001")

    def test_invert(self):
        self.assertEqual(day03.invert([1, 0, 0, 1]), [0, 1, 1, 0])

    def test_filter(self):
        values = [
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(day03.filter(values, [0, 0, 0, 0]), [[0, 0, 0, 0]])
        self.assertEqual(day03.filter(values, [0, 0]), values[:3])
