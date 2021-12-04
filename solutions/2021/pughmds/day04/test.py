from unittest import mock, TestCase, main

sample1 = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def parse():
    '''
    Don't want to have to repeat this...
    '''
    from main import parseInput
    fileText = sample1.replace("\n\n", "\n")
    inputStrings = fileText.split('\n')
    return parseInput(inputStrings, 5)

class TestFirst(TestCase):
    def test_inputParsing(self):
        numbers, inputStrings = parse()
        self.assertEqual(numbers, [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1])
        self.assertEqual(inputStrings[0][0], "22 13 17 11 0")

    def test_boardCreation(self):
        from main import convertInputToBoardGroups
        from main import BingoBoard
        numbers, inputStrings = parse()
        boards = convertInputToBoardGroups(inputStrings)
        self.assertEqual(
            boards[0].board,
            [
                [22, 13, 17, 11, 0],
                [8, 2, 23, 4, 24],
                [21, 9, 14, 16, 7],
                [6, 10, 3, 18, 5],
                [1, 12, 20, 15, 19]
            ])

        self.assertEqual(
            boards[0].check,
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ])

    def test_markNumber(self):
        from main import BingoBoard
        thisBoard = BingoBoard([[1, 2, 3],[4, 5, 6], [7, 8, 9]])
        thisBoard.markNumber(4)
        self.assertEqual(thisBoard.check, [[0, 0, 0],[1, 0, 0],[0, 0, 0]])


    def test_getWinningBoardV1(self):
        from main import convertInputToBoardGroups
        from main import BingoBoard, runGameV1
        numbers, inputStrings = parse()
        boards = convertInputToBoardGroups(inputStrings)
        winningBoard, lastvalue = runGameV1(numbers, boards)
        self.assertEqual(winningBoard.board[0], [14, 21, 17, 24, 4])

        self.assertEqual(winningBoard.returnWinValue(lastvalue), 4512)

class TestSecond(TestCase):
    def test_getWinningBoardV2(self):
        from main import convertInputToBoardGroups
        from main import BingoBoard, runGameV2
        numbers, inputStrings = parse()
        boards = convertInputToBoardGroups(inputStrings)
        winningBoard, lastvalue = runGameV2(numbers, boards)
        self.assertEqual(winningBoard.board[0], [3, 15, 0, 2, 22])

        self.assertEqual(winningBoard.returnWinValue(lastvalue), 1924)

if __name__ == '__main__':
    main()
