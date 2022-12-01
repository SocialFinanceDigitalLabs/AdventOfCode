from unittest import mock, TestCase, main

sample2 = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

class TestFirst(TestCase):
    def test_parse(self):
        from main import parseInput, findLowPoints, calculateScore
        grid = parseInput(sample2)
        lowPoints = findLowPoints(grid)
        result = calculateScore(lowPoints)
        self.assertEqual(result, 15)

    def test_part2(self):
        from main import parseInput, findLowPoints, getBasins
        grid = parseInput(sample2)
        lowPoints = findLowPoints(grid)

        basins = getBasins(lowPoints, grid)

        self.assertEqual(basins, [3,9,9,14])

        value = basins[-1] * basins[-2] * basins[-3]
        self.assertEqual(value, 1134)

if __name__ == '__main__':
    main()