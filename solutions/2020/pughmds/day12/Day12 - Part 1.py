#!/usr/bin/env python
# coding: utf-8

import math

testData1 = '''F10
N3
F7
R90
F11'''

class Ship:
    def __init__(self, startX, startY):
        self.startX = startX
        self.startY = startY
        self.x = startX
        self.y = startY
        self.angle = 0
        
    def turn(self, amt):
        self.angle -= amt
        if self.angle < 0:
            self.angle += 360
        if self.angle >= 360:
            self.angle -= 360
    
    def moveAngle(self, amt):
        xChange = round(amt * math.cos(self.angle * (math.pi / 180)), 2)
        yChange = round(amt * math.sin(self.angle * (math.pi / 180)), 2)
        print([xChange, yChange])
        self.x += xChange
        self.y += yChange
    
    def handleInstruction(self, instr, amt):
        if instr == 'N':
            self.y -= amt
        elif instr == 'S':
            self.y += amt
        elif instr == 'E':
            self.x += amt
        elif instr == 'W':
            self.x -= amt
        elif instr == 'R':
            self.turn(-amt)
        elif instr == 'L':
            self.turn(amt)
        elif instr == 'F':
            self.moveAngle(amt)
            
    def getManhattanDistanceTravelled(self):
        return (self.y - self.startY) + (self.x - self.startX)
    
def openDirections(filename):
    with open(filename,'r') as file:
        data = file.read()
    return data


# Part 1 Test

testShip = Ship(0,0)
directions = testData1.split("\n")
for item in directions:
    instruction = item[0]
    amount = int(item[1:])
    testShip.handleInstruction(instruction, amount)
    print("(%d,%d) angle %d" % (testShip.x, testShip.y, testShip.angle))
    
print(testShip.getManhattanDistanceTravelled())

# Part 1 Real Data
realData = openDirections('day12.txt')
realData.split("\n")
realShip = Ship(0,0)
directions = realData.split("\n")
for item in directions:
    instruction = item[0]
    amount = int(item[1:])
    realShip.handleInstruction(instruction, amount)
    print("(%d,%d) angle %d" % (realShip.x, realShip.y, realShip.angle))
    
print(realShip.getManhattanDistanceTravelled())




