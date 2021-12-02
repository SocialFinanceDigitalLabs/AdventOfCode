#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math

testGridString = '''.#.
..#
###'''

'''
There is probably a way to combine 2d and 3d versions, but 
that's too involved for a daily challenge.
I could also potentially speed this up, but it was
Fast enough to warrant it at this time. I got the answer
pretty quickly for the part 2 final, so not too much of an issue.
I could be a bit more creative with my looping and not storing
things unnecessarily.

I've also read things about using bounding boxes so I'm only looking
at areas which have values. That would save a TON of looping if utilised'''

def parseInput3d(gridString, pocket):
    grid = gridString.split("\n")
    # Make sure values are placed in the middle of space
    gridAdj = math.floor(len(pocket) / 2)
    yAdj = math.floor(len(grid) / 2)
    xAdj = math.floor(len(grid[0]) / 2)
    for rIdx, row in enumerate(grid):
        for cIdx, col in enumerate(row):
            if grid[rIdx][cIdx] == "#":
                #print("Adding 1 at (%d,%d,%d)" % (cIdx+xAdj,rIdx+yAdj,gridAdj))
                pocket[cIdx - xAdj + gridAdj, rIdx - yAdj + gridAdj, gridAdj] = 1                
    return pocket

def parseInput4d(gridString, pocket):
    grid = gridString.split("\n")
    # Make sure values are placed in the middle of space
    gridAdj = math.floor(len(pocket) / 2)
    yAdj = math.floor(len(grid) / 2)
    xAdj = math.floor(len(grid[0]) / 2)
    for rIdx, row in enumerate(grid):
        for cIdx, col in enumerate(row):
            if grid[rIdx][cIdx] == "#":
                #print("Adding 1 at (%d,%d,%d)" % (cIdx+xAdj,rIdx+yAdj,gridAdj))
                pocket[cIdx - xAdj + gridAdj, rIdx - yAdj + gridAdj, gridAdj, gridAdj] = 1                
    return pocket

def checkPosValue(value, limit):
    if value < 0:
        return 0
    elif value >= limit:
        return limit
    return value
    

def checkNeighbours3d(xPos,yPos,zPos,size,pocket):
    # Avoid boundaries
    xStart = checkPosValue(xPos - 1, size)
    xEnd = checkPosValue(xPos + 2, size)
    yStart = checkPosValue(yPos - 1, size)
    yEnd = checkPosValue(yPos + 2, size)
    zStart = checkPosValue(zPos - 1, size)
    zEnd = checkPosValue(zPos + 2, size)
    neighbours = pocket[xStart:xEnd,yStart:yEnd,zStart:zEnd]
    activity = np.sum(neighbours)
    if pocket[xPos][yPos][zPos] == 1:
        activity -= 1
    return activity

def checkNeighbours4d(xPos,yPos,zPos,wPos,size,pocket):
    # Avoid boundaries
    xStart = checkPosValue(xPos - 1, size)
    xEnd = checkPosValue(xPos + 2, size)
    yStart = checkPosValue(yPos - 1, size)
    yEnd = checkPosValue(yPos + 2, size)
    zStart = checkPosValue(zPos - 1, size)
    zEnd = checkPosValue(zPos + 2, size)
    wStart = checkPosValue(wPos - 1, size)
    wEnd = checkPosValue(wPos + 2, size)
    
    neighbours = pocket[xStart:xEnd,yStart:yEnd,zStart:zEnd,wStart:wEnd]
    activity = np.sum(neighbours)
    if pocket[xPos][yPos][zPos][wPos] == 1:
        activity -= 1
    return activity
    
def step3d(pocket,size):
    '''If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. 
    Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. 
    Otherwise, the cube remains inactive.'''
    changes = []
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if pocket[x][y][z] == 1:
                    '''If a cube is active and exactly 2 or 3 of its 
                    neighbors are also active, the cube remains active. 
                    Otherwise, the cube becomes inactive.'''
                    activity = checkNeighbours3d(x,y,z,size,pocket)
                    if activity < 2 or activity > 3:
                        #print("flip to 0 (%d,%d,%d)" % (x,y,z))
                        changes.append((x,y,z,0))
                    
                else:
                    '''If a cube is inactive but exactly 3 of its 
                    neighbors are active, the cube becomes active. 
                    Otherwise, the cube remains inactive.'''
                    activity = checkNeighbours3d(x,y,z,size,pocket)
                    if activity == 3:
                        #print("flip to 1 (%d,%d,%d)" % (x,y,z))
                        changes.append((x,y,z,1))
                            
    return changes

def step4d(pocket,size):
    '''If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. 
    Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. 
    Otherwise, the cube remains inactive.'''
    changes = []
    for x in range(size):
        for y in range(size):
            for z in range(size):
                for w in range(size):
                    if pocket[x][y][z][w] == 1:
                        '''If a cube is active and exactly 2 or 3 of its 
                        neighbors are also active, the cube remains active. 
                        Otherwise, the cube becomes inactive.'''
                        activity = checkNeighbours4d(x,y,z,w,size,pocket)
                        if activity < 2 or activity > 3:
                            #print("flip to 0 (%d,%d,%d)" % (x,y,z))
                            changes.append((x,y,z,w,0))

                    else:
                        '''If a cube is inactive but exactly 3 of its 
                        neighbors are active, the cube becomes active. 
                        Otherwise, the cube remains inactive.'''
                        activity = checkNeighbours4d(x,y,z,w,size,pocket)
                        if activity == 3:
                            #print("flip to 1 (%d,%d,%d)" % (x,y,z))
                            changes.append((x,y,z,w,1))
                            
    return changes

def applyChanges3d(changeList,pocket):
    for c in changeList:
        x,y,z,v = c
        pocket[x][y][z] = v
    return pocket

def applyChanges4d(changeList,pocket):
    for c in changeList:
        x,y,z,w,v = c
        pocket[x][y][z][w] = v
    return pocket

def openFile(filename):
    with open (filename, 'r') as file:
        data = file.read()
    return data

# Part 1 test
print("==== PART 1 - TEST ====")
size = 3*5
pocket = np.zeros((size,size,size))
pocket = parseInput3d(testGridString, pocket)
print("-----INIT------")
print(np.sum(pocket))
for i in range(1,7):    
    print("-----STEP %d------" % (i))
    changeList = step3d(pocket,size)
    pocket = applyChanges3d(changeList,pocket)
    print(np.sum(pocket))

# Part 1
print("==== PART 1 - REAL ====")
gridString = openFile("day17.txt")
size = 8*5
pocket = np.zeros((size,size,size))
pocket = parseInput3d(gridString, pocket)
print("-----INIT------")
print(np.sum(pocket))
for i in range(1,7):    
    print("-----STEP %d------" % (i))
    changeList = step3d(pocket,size)
    pocket = applyChanges3d(changeList,pocket)
    print(np.sum(pocket))


# Part 2 test
print("==== PART 2 - TEST ====")
size = 3*5
pocket = np.zeros((size,size,size,size))
pocket = parseInput4d(testGridString, pocket)
print("-----INIT------")
print(np.sum(pocket))
for i in range(1,7):    
    print("-----STEP %d------" % (i))
    changeList = step4d(pocket,size)
    pocket = applyChanges4d(changeList,pocket)
    print(np.sum(pocket))


# Part 2 test
print("==== PART 2- REAL ====")
gridString = openFile("day17.txt")
size = 8*5
pocket = np.zeros((size,size,size,size))
pocket = parseInput4d(gridString, pocket)
print("-----INIT------")
print(np.sum(pocket))
for i in range(1,7):    
    print("-----STEP %d------" % (i))
    changeList = step4d(pocket,size)
    pocket = applyChanges4d(changeList,pocket)
    print(np.sum(pocket))





