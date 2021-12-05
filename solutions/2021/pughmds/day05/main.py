from bresenham import bresenham

def parseInput(input):
    inputStrings = input.split('\n')
    biggest = 0
    coordinates = []
    for i in inputStrings:
        pointStrings = i.split("->")
        line = []
        for p in pointStrings:
            x, y = map(int, p.strip().split(","))
            if x > biggest:
                biggest = x
            if y > biggest:
                biggest = y
            line.append([x, y])
        coordinates.append(line)
    return biggest, coordinates

def filterOutDiagonals(coordinates):
    horizAndVertCoords = []
    for line in coordinates:
        if line[0][0] != line[1][0] and line[0][1] != line[1][1]:
            #This is a diagonal line, and we need to remove it
            continue
        else:
            horizAndVertCoords.append(line)
    return horizAndVertCoords

class Grid:
    def __init__(self, size):
        self.setupMap(size+1)

    def setupMap(self, size):
        '''
            Zero-fill the entire map to start
        '''
        self.map = []
        for r in range(0, size):
            self.map.append([0 for c in range(0, size)])

    def placeCoordinate(self, x, y):
        self.map[x][y] += 1

    def placeLine(self, line):
        '''
            A line consists of two coordinates. Using Bresenham's Line Algorithm,
            We can get the points in between those two coordinates pretty easily
        '''
        a = line[0]
        b = line[1]
        points = list(bresenham(a[0], a[1], b[0], b[1]))
        for p in points:
            self.placeCoordinate(p[0], p[1])

    def findOverlaps(self):
        count = 0
        for x in self.map:
            for y in x:
                if y >= 2:
                    count += 1
        return count

if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    print("----PART 1-----")
    biggest, coordinates = parseInput(fileText)
    coords = filterOutDiagonals(coordinates)
    part1Grid = Grid(biggest)

    for line in coords:
        part1Grid.placeLine(line)

    result = part1Grid.findOverlaps()
    print(result)

    print("----PART 2-----")
    biggest, coordinates = parseInput(fileText)
    part2Grid = Grid(biggest)
    
    for line in coordinates:
        part2Grid.placeLine(line)
    
    result = part2Grid.findOverlaps()
    print(result)