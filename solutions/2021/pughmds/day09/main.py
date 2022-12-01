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

def findLowPoints(grid):
    '''
    Simple code to find low points by just comparing
    with the tiles around it (not diagonally)
    '''
    lowPoints = []
    for y, line in enumerate(grid):
        for x, pos in enumerate(line):
            check = 0
            if y - 1 >= 0:
                if grid[y-1][x] <= grid[y][x]:
                    check -= 1
            if x - 1 >= 0:
                if grid[y][x-1] <= grid[y][x]:
                    check -= 1
            if y + 1 < len(grid):
                if grid[y+1][x] <= grid[y][x]:
                    check -= 1
            if x + 1 < len(line):
                if grid[y][x+1] <= grid[y][x]:
                    check -= 1
            if check == 0:
                lowPoints.append({'x': x, 'y': y, 'value': grid[y][x]})
    return lowPoints

def follow(row, col, pointsInBasin, grid):
    '''
    A bit of recursion (hope it doesn't break python)
    to start at the low points and expand out until we hit 9s,
    keeping a tally the entire time
    '''
    rowsInGrid = len(grid)
    colsInGrid = len(grid[0])
    for y, x in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if (row + y, col + x) not in pointsInBasin:
            if row + y >= 0 and row + y < rowsInGrid:
                if col + x < colsInGrid and col + x >= 0:
                    if grid[row + y][col + x] != 9:
                        pointsInBasin.append((row + y, col + x))
                        follow(row + y, col + x, pointsInBasin, grid)
    return pointsInBasin

def calculateScore(lowPoints):
    '''
    Calculate the part 1 score using the low points
    '''
    sum = 0
    for low in lowPoints:
        sum += low["value"] + 1

    return sum

def getBasins(lowPoints, grid):
    '''
    Each basin starts at a low point.
    Starting there, use follow to expand and
    count how big they are.
    '''
    basins = []
    for low in lowPoints:
        pointsInBasin = [(low["y"], low["x"])]
        basin = follow(low["y"], low["x"], pointsInBasin, grid)
        basinSize = len(basin)
        basins.append(basinSize)
    return sorted(basins)

if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    print("----PART 1-----")
    grid = parseInput(fileText)
    lowPoints = findLowPoints(grid)
    result = calculateScore(lowPoints)
    print(result)

    print("----PART 2-----")
    basins = getBasins(lowPoints, grid)
    value = basins[-1] * basins[-2] * basins[-3]
    print(value)