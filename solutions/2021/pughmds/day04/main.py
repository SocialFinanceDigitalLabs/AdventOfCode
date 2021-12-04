'''
    I'm probably overcomplicating this solution, but hey...it works, so
    I'm not streamlining it any more than I need to.  :-)

    I could also probably do this faster with numpy, but it wouldn't install,
    so I was limited to core libraries.
'''

def convertInputToBoardGroups(input):
    boards = []
    for b in input:
        for idx, row in enumerate(b):
            b[idx] = b[idx].strip().replace("  ", " ").split(" ")
            b[idx] = list(map(int, b[idx]))
        i = BingoBoard(b)
        boards.append(i)
    return boards

def runGameV1(numbers, boards):
    '''
    Which board wins first?
    '''
    for n in numbers:
        for b in boards:
            b.markNumber(n)
            b.checkWin()
            if b.won:
                return b, n
    return False, False

def runGameV2(numbers, boards):
    '''
    Which board wins last?
    '''
    totalBoards = len(boards)
    wonCount = 0

    for n in numbers:
        for b in boards:
            if not b.won:
                b.markNumber(n)
                b.checkWin()
                if b.won:
                    wonCount += 1
                    if wonCount == totalBoards:
                        return b, n
    return False, False

def parseInput(inputStrings, boardHeight):
    '''
    Separating out the first line as input numbers, and then handling thbe rest as bingo boards
    '''
    for idx, item in enumerate(inputStrings):
        inputStrings[idx] = item.replace("  ", " ")

    numbers = list(map(int, inputStrings[0].split(",")))
    inputStrings = inputStrings[1:]
    boardInputs = [inputStrings[x:x + boardHeight] for x in range(0, len(inputStrings), boardHeight)]
    return numbers, boardInputs

class BingoBoard:
    def __init__(self, numbers):
        self.board = numbers
        self.won = False
        self.boardSize = len(numbers)
        self.resetCheck()
        self.boardSize = len(numbers)

    def resetCheck(self):
        '''
        Resets the board for a new game
        '''
        self.check = []
        for r in range(0, self.boardSize):
            self.check.append([0 for c in range(0, self.boardSize)])

    def markNumber(self, num):
        '''
        Marks a number on the board as found
        '''
        for rowidx, row in enumerate(self.board):
            if num in row:
                self.check[rowidx][row.index(num)] = 1
                return

    def checkWin(self):
        '''
        Checks to see if the board won
        '''
        for row in self.check:
            if sum(row) >= self.boardSize:
                self.won = True
                return
        colCheck = list(map(sum, zip(*self.check)))
        if self.boardSize in colCheck:
            self.won = True
            return

    def returnWinValue(self, drawnNumber):
        '''
        Calculates the traditionally strange value AdventOfCode wants to check the answer
        '''
        runningTotal = 0
        for rowidx, row in enumerate(self.check):
            for colidx, col in enumerate(row):
                if col == 0:
                    runningTotal += self.board[rowidx][colidx]
        return runningTotal * drawnNumber

if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()
        fileText = fileText.replace("\n\n","\n")
        inputStrings = fileText.split('\n')

    numbers, inputStrings = parseInput(inputStrings, 5)
    boards = convertInputToBoardGroups(inputStrings)

    print("----PART 1-----")
    winningBoard, lastvalue = runGameV1(numbers, boards)
    result = winningBoard.returnWinValue(lastvalue)
    print(result)

    print("----PART 2-----")
    # Let's reset the boards
    for b in boards:
        b.resetCheck()
        b.won = False
    winningBoard, lastValue = runGameV2(numbers, boards)
    result = winningBoard.returnWinValue(lastValue)
    print(result)
