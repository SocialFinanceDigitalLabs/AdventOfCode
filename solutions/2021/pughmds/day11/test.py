from unittest import mock, TestCase, main

sample0 = """11111
19991
19191
19991
11111"""

sample1 = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

class TestFirst(TestCase):
    def test_calculate_score(self):
        from main import parseInput, step
        grid = parseInput(sample0)

        # For each existing 10, add 1 to each surrounding cell
        flashedCount = 0
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 9)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 9)

    def test_calculate_larger_score(self):
        from main import parseInput, step
        grid = parseInput(sample1)

        # For each existing 10, add 1 to each surrounding cell
        flashedCount = 0
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 0)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16 + 8)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16 + 8 + 1)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16 + 8 + 1 + 7)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16 + 8 + 1 + 7 + 24)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16 + 8 + 1 + 7 + 24 + 39)
        grid, flashedCount = step(grid, flashedCount)
        self.assertEqual(flashedCount, 35 + 45 + 16 + 8 + 1 + 7 + 24 + 39 + 29)
        self.assertEqual(grid,[[0,4,8,1,1,1,2,9,7,6],
                [0,0,3,1,1,1,2,0,0,9],
                [0,0,4,1,1,1,2,5,0,4],
                [0,0,8,1,1,1,1,4,0,6],
                [0,0,9,9,1,1,1,3,0,6],
                [0,0,9,3,5,1,1,2,3,3],
                [0,4,4,2,3,6,1,1,3,0],
                [5,5,3,2,2,5,2,3,5,0],
                [0,5,3,2,2,5,0,6,0,0],
                [0,0,3,2,2,4,0,0,0,0]
           ]
         )


if __name__ == '__main__':
    main()