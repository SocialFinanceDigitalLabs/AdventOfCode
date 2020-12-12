#!/usr/bin/env python
# coding: utf-8

import math

testData1 = '''F10
N3
F7
R90
F11'''

class Ship:
    def __init__(self, startX, startY, waypointX, waypointY):
        self.startX = startX
        self.startY = startY
        self.waypointX = waypointX
        self.waypointY = waypointY
        self.x = startX
        self.y = startY
        
    def turn(self, amt):
        angle = math.radians(amt)
        tmpX = self.waypointX
        tmpY = self.waypointY
        self.waypointX = math.cos(angle) * (tmpX - self.x) - math.sin(angle) * (tmpY - self.y) + self.x
        self.waypointY = self.y + (math.sin(angle) * (tmpX - self.x) + math.cos(angle) * (tmpY - self.y))
        
    def move(self, amt):
        diffX = (self.waypointX - self.x)
        diffY = (self.waypointY - self.y)
        self.x += diffX * amt
        self.y += diffY * amt
        self.waypointX = self.x + diffX
        self.waypointY = self.y + diffY
    
    def handleInstruction(self, instr, amt):
        if instr == 'N':
            print("Moving waypoint north %d" % (amt))
            self.waypointY -= amt
        elif instr == 'S':
            print("Moving waypoint south %d" % (amt))
            self.waypointY += amt
        elif instr == 'E':
            print("Moving waypoint east %d" % (amt))
            self.waypointX += amt
        elif instr == 'W':
            print("Moving waypoint west %d" % (amt))
            self.waypointX -= amt
        elif instr == 'R':
            self.turn(amt)
        elif instr == 'L':
            self.turn(-amt)
        elif instr == 'F':
            self.move(amt) 
            
    def getManhattanDistanceTravelled(self):
        return (self.y - self.startY) + (self.x - self.startX)
    
def openDirections(filename):
    with open(filename,'r') as file:
        data = file.read()
    return data


# Part 2 Test
testShip = Ship(0,0,10,-1)
directions = testData1.split("\n")
for item in directions:
    instruction = item[0]
    amount = int(item[1:])
    print("Next instruction %s" % (item))
    testShip.handleInstruction(instruction, amount)
    print("Ship: (%d,%d) Waypoint: (%d, %d)" % (testShip.x, testShip.y, testShip.waypointX, testShip.waypointY))
    
print(testShip.getManhattanDistanceTravelled())

# Part 2 Real Data
realData = openDirections('day12.txt')
realData.split("\n")
realShip = Ship(0,0,10,-1)
directions = realData.split("\n")
for item in directions:
    instruction = item[0]
    amount = int(item[1:])
    print("Next instruction %s" % (item))
    realShip.handleInstruction(instruction, amount)
    print("Ship: (%d,%d) Waypoint: (%d, %d)" % (realShip.x, realShip.y, realShip.waypointX, realShip.waypointY))
    
print(realShip.getManhattanDistanceTravelled())




