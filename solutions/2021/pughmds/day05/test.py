from unittest import mock, TestCase, main
import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True)

sample0 = """1,3 -> 3,3
2,0 -> 0,2
3,0 -> 3,2"""

sample1 = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

class TestFirst(TestCase):
    def test_inputParsing(self):
        from main import parseInput
        biggest, coordinates = parseInput(sample1)
        self.assertEqual(biggest, 9)

        self.assertEqual(coordinates[0], [[0,9], [5,9]])

    def test_filterDiagonals(self):
        from main import parseInput, filterOutDiagonals
        biggest, coordinates = parseInput(sample0)
        result = filterOutDiagonals(coordinates)

        self.assertEqual(result, [[[1, 3],[3, 3]], [[3, 0],[3, 2]]])

    def test_markGrid(self):
        from main import parseInput, Grid, filterOutDiagonals
        biggest, coordinates = parseInput(sample0)
        coords = filterOutDiagonals(coordinates)
        testGrid = Grid(biggest)

        for line in coords:
            testGrid.placeLine(line)

        self.assertEqual(testGrid.map, [[0,0,0,0],[0,0,0,1],[0,0,0,1],[1,1,1,1]])

    def test_v1(self):
        from main import parseInput, Grid, filterOutDiagonals
        biggest, coordinates = parseInput(sample1)
        coords = filterOutDiagonals(coordinates)
        testGrid = Grid(biggest)

        for line in coords:
            testGrid.placeLine(line)

        result = testGrid.findOverlaps()
        print("Map for V1")
        pp.pprint(testGrid.map)
        self.assertEqual(result, 5)

    def test_v2(self):
        from main import parseInput, Grid
        biggest, coordinates = parseInput(sample1)
        testGrid = Grid(biggest)

        for line in coordinates:
            testGrid.placeLine(line)

        result = testGrid.findOverlaps()
        print("Map for V2")
        pp.pprint(testGrid.map)
        self.assertEqual(result, 12)

if __name__ == '__main__':
    main()
