#!/usr/bin/env python
# coding: utf-8

import re
import math

testSlope = [
    "..##.......",
    "#...#...#..",
    ".#....#..#.",
    "..#.#...#.#",
    ".#...##..#.",
    "..#.##.....",
    ".#.#.#....#",
    ".#........#",
    "#.##...#...",
    "#...##....#",
    ".#..#...#.#"
]

startPoint = [0,0]
runSlope = [[3,1],[1,1],[5,1],[7,1],[1,2]]
slopeWidth = len(testSlope[0])
endY = len(testSlope)

def getTreeCoordinates(slopeMap):
    treeCoordinates = []
    for num, row in enumerate(slopeMap):
        trees = [m.start() for m in re.finditer('#', row)]
        for tree in trees:
            treeCoordinates.append([tree,num])
            
    return treeCoordinates
    
def getTobogganRun(slope, endY):
    coordinates = []
    for y in range(endY):
        x = (y * slope)
        coordinates.append([x,y])
    return coordinates

def determineSlope(runSlope, startPoint):
    return (runSlope[0] - startPoint[0]) / (runSlope[1] - startPoint[1])

def countTrees(runCoordinates, treeMap, slopeWidth):
    treeCount = 0
    for tree in treeMap:
        for position in runCoordinates:
            if tree[0] == position[0] % slopeWidth and tree[1] == position[1]:
                treeCount += 1
                
    return treeCount


def splitInput(filename):
  with open(filename, 'r') as fileStream:
    fileText = fileStream.read()
    inputStrings = fileText.split('\n')

  return inputStrings
    
# Validate test

foundTrees = getTreeCoordinates(testSlope)
slope = determineSlope(runSlope[0], startPoint)
runCoordinates = getTobogganRun(slope, endY)

print(countTrees(runCoordinates, foundTrees, slopeWidth))

# Part 1 run
realSlope = splitInput("day3.txt")
slopeWidth = len(realSlope[0])
endY = len(realSlope)
foundTrees = getTreeCoordinates(realSlope)
slope = determineSlope(runSlope[0], startPoint)
runCoordinates = getTobogganRun(slope, endY)

print(countTrees(runCoordinates, foundTrees, slopeWidth))

# Part 2 Test Run
slopeWidth = len(testSlope[0])
endY = len(testSlope)
treesHit = []
for num, thisRunSlope in enumerate(runSlope):
    foundTrees = getTreeCoordinates(testSlope)
    print(foundTrees)
    slope = determineSlope(thisRunSlope, startPoint)
    runCoordinates = getTobogganRun(slope, endY)
    print(runCoordinates)

    trees = countTrees(runCoordinates, foundTrees, slopeWidth)
    print(trees)
    treesHit.append(trees)
    
print("Product of trees hit: %d" % (math.prod(treesHit)))


# Part 2 Real run
slopeWidth = len(realSlope[0])
endY = len(realSlope)
treesHit = []
for num, thisRunSlope in enumerate(runSlope):
    print(thisRunSlope)
    realSlope = splitInput("day3.txt")
    slopeWidth = len(realSlope[0])
    endY = len(realSlope)
    foundTrees = getTreeCoordinates(realSlope)
    slope = determineSlope(thisRunSlope, startPoint)
    runCoordinates = getTobogganRun(slope, endY)
    trees = countTrees(runCoordinates, foundTrees, slopeWidth)
    print(trees)
    
    treesHit.append(trees)
    
print(treesHit)
print("Product of trees hit: %d" % (math.prod(treesHit)))




