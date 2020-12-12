#!/usr/bin/env python
# coding: utf-8

import copy
import numpy as np

testSeatString = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''

def openFile(filename):
    with open(filename, 'r') as file:
        return file.read()

def parseInput(seatString):
    seats = seatString.split("\n")
    for i, s in enumerate(seats):
        seats[i] = [char for char in s]
    return seats

class Lounge:
    def __init__(self, seatArray):
        self.seatArray = []
        self.seatArray.append(seatArray)
        self.time = 0
        
    def checkSeat(self, subGroup):
        occupied = sum(x.count('#') for x in subGroup)
        if subGroup[1][1] == "#":
            occupied -= 1
        return occupied
    
    def printSeats(self):
        print(np.matrix(self.seatArray[self.time]))
        
    def findSurroundingSeats(self, row, col):
        #print("(%d,%d)" % (col,row))
        subGroup = [
            [".",".","."],
            [".",".","."],
            [".",".","."]
        ]
        
        subGroup[1][1] = self.seatArray[self.time][row][col]
        
        # We need to find if there are any seats in each direction and assume they're
        # directly next door in the subGroup so we can reuse the code from part 1

	# this is horrible code, but it works.  Could probably make this MUCH more
	# efficient if I wanted to / had the time.
        
        # First, straight up:
        foundSeat = False
        tempRow = row
        while not foundSeat:
            tempRow -= 1
            if tempRow >= 0:
                if self.seatArray[self.time][tempRow][col] in ["#","L"]:
                    subGroup[0][1] = self.seatArray[self.time][tempRow][col]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[0][1] = "."
                foundSeat = True
        
        # straight down:
        foundSeat = False
        tempRow = row
        while not foundSeat:
            tempRow += 1
            if tempRow < len(self.seatArray[self.time]):
                if self.seatArray[self.time][tempRow][col] in ["#","L"]:
                    subGroup[2][1] = self.seatArray[self.time][tempRow][col]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[2][1] = "."
                foundSeat = True
            
        # left
        foundSeat = False
        tempCol = col
        while not foundSeat:
            tempCol -= 1
            if tempCol >= 0:
                if self.seatArray[self.time][row][tempCol] in ["#","L"]:
                    subGroup[1][0] = self.seatArray[self.time][row][tempCol]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[1][0] = "."
                foundSeat = True

        # right
        foundSeat = False
        tempCol = col
        while not foundSeat:
            tempCol += 1
            if tempCol < len(self.seatArray[self.time][row]):
                if self.seatArray[self.time][row][tempCol] in ["#","L"]:
                    subGroup[1][2] = self.seatArray[self.time][row][tempCol]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[1][2] = "."
                foundSeat = True

        # upper left
        foundSeat = False
        tempCol = col
        tempRow = row
        while not foundSeat:
            tempCol -= 1
            tempRow -= 1
            if tempRow >= 0 and tempCol >= 0:
                if self.seatArray[self.time][tempRow][tempCol] in ["#","L"]:
                    subGroup[0][0] = self.seatArray[self.time][tempRow][tempCol]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[0][0] = "."
                foundSeat = True

        # upper right
        foundSeat = False
        tempCol = col
        tempRow = row
        while not foundSeat:
            tempCol += 1
            tempRow -= 1
            if tempRow >= 0 and tempCol < len(self.seatArray[self.time][tempRow]):
                if self.seatArray[self.time][tempRow][tempCol] in ["#","L"]:
                    subGroup[0][2] = self.seatArray[self.time][tempRow][tempCol]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[0][2] = "."
                foundSeat = True

        # bottom left
        foundSeat = False
        tempCol = col
        tempRow = row
        while not foundSeat:
            tempCol -= 1
            tempRow += 1
            if tempCol >= 0 and tempRow < len(self.seatArray[self.time]):
                if self.seatArray[self.time][tempRow][tempCol] in ["#","L"]:
                    subGroup[2][0] = self.seatArray[self.time][tempRow][tempCol]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[2][0] = "."
                foundSeat = True
                
        # bottom right
        foundSeat = False
        tempCol = col
        tempRow = row
        while not foundSeat:
            tempCol += 1
            tempRow += 1
            if tempRow < len(self.seatArray[self.time]) and tempCol < len(self.seatArray[self.time][tempRow]):
                if self.seatArray[self.time][tempRow][tempCol] in ["#","L"]:
                    subGroup[2][2] = self.seatArray[self.time][tempRow][tempCol]
                    foundSeat = True
                else:
                    continue
            else:
                subGroup[2][2] = "."
                foundSeat = True                
                
        #print(np.matrix(subGroup))
        return subGroup
        
    def stepSeats(self):
        self.seatArray.append(copy.deepcopy(self.seatArray[self.time]))
        for rowIdx, row in enumerate(self.seatArray[self.time]):
            for colIdx, col in enumerate(row):
                if self.seatArray[self.time][rowIdx][colIdx] == ".":
                    continue
                else:
                    subGroup = self.findSurroundingSeats(rowIdx, colIdx)
                            
                    result = self.checkSeat(subGroup)
                    
                    if self.seatArray[self.time][rowIdx][colIdx] == "L":
                        if result == 0:
                            self.seatArray[self.time + 1][rowIdx][colIdx] = "#"
                    elif self.seatArray[self.time][rowIdx][colIdx] == "#":
                        if result >= 5:
                            self.seatArray[self.time + 1][rowIdx][colIdx] = "L"
        self.time += 1
    
    def swapValue(self, row, col, i, j, seat):
        if row + i - 1 < 0:
            return "." 
        elif row + i - 1 >= len(seat):
            return "." 
        elif col + j - 1 < 0:  
            return "." 
        elif row + i - 1 >= len(seat):
            return "." 
        elif col + j - 1 >= len(seat[row + i - 1]):
            return "." 
        else:
            return seat[row + i - 1][col + j - 1]    
    
    def testForDuplicates(self):
        if len(self.seatArray) == 1:
            return False
        for step in self.seatArray[:-1]:
            if step == self.seatArray[-1]:
                return True
        return False
    
    def runUntilRepeat(self):
        count = 0
        while True:
            print("This is iteration number %d" % (count + 1))
            self.printSeats()
            self.stepSeats()
            if self.testForDuplicates():
                return count
            if count > 10000:
                return -1
            count += 1

    def countSeatsAtIndex(self, index):
        occupied = 0
        for row in self.seatArray[index]:
            occupied += sum(x.count('#') for x in row)
        return occupied

# Part 1 Test
testSeats = parseInput(testSeatString)
testLounge = Lounge(testSeats)
index = testLounge.runUntilRepeat()
seatCount = testLounge.countSeatsAtIndex(index)
print("The number of occupied seats once stabilised at index %d is %d" % (index, seatCount))

realSeatString = openFile('day11.txt')
realSeats = parseInput(realSeatString)
realLounge = Lounge(realSeats)
index = realLounge.runUntilRepeat()
seatCount = realLounge.countSeatsAtIndex(index)
print("The number of occupied seats once stabilised at index %d is %d" % (index, seatCount))



