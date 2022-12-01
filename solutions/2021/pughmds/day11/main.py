def parseInput(inputText):
    '''
    Parse the input string into a simple 2D
    List. No need for anything like numpy I hope
    '''
    grid = []
    inputLines = inputText.split("\n")
    for line in inputLines:
        gridLine = []
        for i, v in enumerate(line):
            gridLine.append(int(v))
        grid.append(gridLine)
    return grid

def flashTransfer(grid, row, col):
    rowsInGrid = len(grid)
    colsInGrid = len(grid[0])

    for y, x in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        if row + y >= 0 and row + y < rowsInGrid:
            if col + x < colsInGrid and col + x >= 0:
                grid[row + y][col + x] += 1
    return grid

def step(grid, flashedCount):
    for rIdx, row in enumerate(grid):
        for cIdx, col in enumerate(row):
            grid[rIdx][cIdx] += 1

    done = False
    while not done:
        for rIdx, row in enumerate(grid):
            for cIdx, col in enumerate(row):
                if grid[rIdx][cIdx] > 9 and grid[rIdx][cIdx] < 999:
                    grid = flashTransfer(grid, rIdx, cIdx)
                    grid[rIdx][cIdx] = 999
        done = True
        for rIdx, row in enumerate(grid):
            for cIdx, col in enumerate(row):
                if grid[rIdx][cIdx] > 9 and grid[rIdx][cIdx] < 999:
                    done = False


    for rIdx, row in enumerate(grid):
        for cIdx, col in enumerate(row):
            if grid[rIdx][cIdx] >= 999:
                grid[rIdx][cIdx] = 0
                flashedCount += 1
    return grid, flashedCount

if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    grid = parseInput(fileText)
    print("----PART 1-----")
    # For each existing 10, add 1 to each surrounding cell
    flashedCount = 0
    for i in range(0,100):
        grid, flashedCount = step(grid, flashedCount)

    print(flashedCount)
    print("----PART 2-----")
    grid = parseInput(fileText)
    flashedCount = 0
    done = False
    stepCount = 0
    while not done:
        grid, flashedCount = step(grid, flashedCount)
        stepCount += 1
        if sum(map(sum, grid)) == 0:
            print(stepCount)
            done = True