#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math


def openFile(filename):
    with open(filename, "r") as file:
        data = file.read()
    return data
        
def parseInput(tileString):
    processedTiles = []
    tiles = tileString.split("\n\n")
    #The first line should have the tile number
    for tile in tiles:
        tileLines = tile.split("\n")
        tileNum = int(tileLines[0][tileLines[0].index(" "):].replace(":","").strip())
        thisTile = Tile(tileNum, tileLines[1:])
        processedTiles.append(thisTile)
    return processedTiles
        
        
class Tile:
    # Handling each individual tile...
    def __init__(self, tileNum, tileArray):
        self.number = int(tileNum)
        self.pattern = tileArray
        self.originalPattern = tileArray
        
        # Next, we need to store the edges:
        self.edges = {
            "top": {"pattern": self.pattern[0], "tileMatches": []},
            "bottom": {"pattern": self.pattern[-1][::-1], "tileMatches": []},
            "right": {"pattern": ''.join([x[len(self.pattern[0]) -1] for x in self.pattern]), "tileMatches": []},
            "left": {"pattern": ''.join([x[0] for x in self.pattern][::-1]), "tileMatches": []}
        }
        
    def checkMatch(self, testTile):
        if testTile.number == self.number:
            return
        for direction in testTile.edges.keys():
            for edge in self.edges.keys():
                # Match as input
                if self.edges[direction]["pattern"] == testTile.edges[edge]["pattern"]:
                    self.edges[direction]["tileMatches"].append(testTile.number)

                # Match if flipped...store as negative so we remember to flip
                if self.edges[direction]["pattern"] == testTile.edges[edge]["pattern"][::-1]:
                    self.edges[direction]["tileMatches"].append(-testTile.number)
            
        
    def countTotalMatches(self):
        count = 0
        for edge in self.edges.keys():
            count += len(self.edges[edge]["tileMatches"])
        return count
    
    def rotate(self, orient):
        newGrid = []
        if self.number == 2729:
            print("-------------------------")
            print(*self.pattern, sep="\n")
            print(self.edges)
            print("rrrrrrrrrrrrrrrrrrrrrrrrr")
        
        if orient == 0:
            return True
        elif orient == 2:
            print("Rotating 180 degres")
            # Orient 2: rotate the grid
            for g in self.pattern[::-1]:
                newGrid.append(''.join(g[::-1]))
            self.pattern = newGrid
            # Next, we need to rotate the edges
            newEdge = {}
            newEdge["top"] = self.edges["bottom"]
            newEdge["left"] = self.edges["right"]
            newEdge["right"] = self.edges["left"]
            newEdge["bottom"] = self.edges["top"]
            self.edges = newEdge
        elif orient == 1:
            print("Rotating right 90 degrees")
            # Orient 1: rotate the grid
            newGrid = list(zip(*self.pattern[::-1]))
            #print(np.array(newGrid))
            self.pattern = newGrid
            
            # Next, we need to rotate the edges
            newEdge = {}
            newEdge["top"] = self.edges["left"]
            newEdge["right"] = self.edges["top"]
            newEdge["bottom"] = self.edges["right"]
            newEdge["left"] = self.edges["bottom"]
            self.edges = newEdge
        elif orient == -1 or orient == 3:
            print("Rotating left 90 degrees")
            # Orient -1: rotate the grid
            newGrid = list(zip(*self.pattern))[::-1]
            #print(np.array(newGrid))
            self.pattern = newGrid
            
            # Next, we need to rotate the edges
            newEdge = {}
            newEdge["bottom"] = self.edges["left"]
            newEdge["right"] = self.edges["bottom"]
            newEdge["top"] = self.edges["right"]
            newEdge["left"] = self.edges["top"]
            self.edges = newEdge 
        if self.number == 2729:
            print("RRRRRRRRRRRRRRRRRRRRRRRRR")
            print(*self.pattern, sep="\n")
            print(self.edges)
            print("-------------------------")
            
    def flip(self, axis):
        if axis == 1:
            # Flip the x values
            print("Flipping left-right...")
            newGrid = []
            for g in self.pattern:
                newGrid.append(g[::-1])
            self.pattern = newGrid 
            
            newEdge = {}
            newEdge["bottom"] = self.edges["bottom"]
            newEdge["bottom"]["pattern"] = newEdge["bottom"]["pattern"][::-1]
            for idx, item in enumerate(newEdge["bottom"]["tileMatches"]):
                newEdge["bottom"]["tileMatches"][idx] *= -1
            newEdge["left"] = self.edges["right"]
            newEdge["right"] = self.edges["left"]
            newEdge["top"] = self.edges["top"]
            newEdge["top"]["pattern"] = newEdge["top"]["pattern"][::-1]
            for idx, item in enumerate(newEdge["top"]["tileMatches"]):
                newEdge["top"]["tileMatches"][idx] *= -1
            self.edges = newEdge
        if axis == 2:
            # Flip the y values
            print("Flipping top-bottom...")
            
            if self.number == 2729:
                print("-------------------------")
                print(*self.pattern, sep="\n")
                print(self.edges)
                print("vvvvvvvvvvvvvvvvvvvvvvvvv")
                
            newGrid = []
            for g in self.pattern[::-1]:
                newGrid.append(g)
            self.pattern = newGrid
                
            newEdge = {}
            newEdge["bottom"] = self.edges["top"]
            newEdge["left"] = self.edges["left"]
            newEdge["left"]["pattern"] = newEdge["left"]["pattern"][::-1]
            for idx, item in enumerate(newEdge["left"]["tileMatches"]):
                newEdge["left"]["tileMatches"][idx] *= -1
            newEdge["right"] = self.edges["right"]
            newEdge["right"]["pattern"] = newEdge["right"]["pattern"][::-1]
            for idx, item in enumerate(newEdge["right"]["tileMatches"]):
                newEdge["right"]["tileMatches"][idx] *= -1
            newEdge["top"] = self.edges["bottom"]
            self.edges = newEdge     
            
            if self.number == 2729:
                print("^^^^^^^^^^^^^^^^^^^^^^^^^")
                print(*self.pattern, sep="\n")
                print(self.edges)
                print("-------------------------")
            
    def fixEdges(self):
        for edge in self.edges.keys():
            self.edges[edge]["tileMatches"] = [abs(x) for x in self.edges[edge]["tileMatches"]]


class Map:
    # This will be where we assemble the tiles in the right order
    def __init__(self, width, height):
        self.image = [[None for i in range(width)] for j in range(height)]
        self.tileNumberMap = [[None for i in range(width)] for j in range(height)]
        self.width = width
        self.height = height
        
    def placeTile(self, tile, xpos, ypos):
        self.image[ypos][xpos] = tile
        
    def addTile(self,x,y,tile,orient,flipAxis):
        print("Adding tile %d at (%d,%d) and r(%d), f(%d)" % (tile.number, x, y, orient, flipAxis))
        try:
            self.tileNumberMap[y][x] = tile.number
        except:
            print("Problem at (%d,%d)" % (x,y))
        
        # Now, we need to rotate the tile so it fits correctly
        tile.flip(flipAxis)
        if flipAxis != 0 and orient < 2:
            # If we flipt the tile, the rotation also flips
            orient *= -1
        tile.rotate(orient)
        #tile.fixEdges()
        self.image[y][x] = tile
    
    def printTileNumberMap(self):
        print(np.array(self.tileNumberMap))
        
    def printImage(self):
        outline = 0
        for yIdx, imageRow in enumerate(self.image):
            line = ""
            for xIdx, item in enumerate(imageRow):
                if item is None:
                    line += "----------"
                else:
                    line += item.pattern[outLine%10]
        
    def placeFirstCorner(self, corners, tiles):
        for tile in tiles:
            if tile.number == calc[0]:
                #print(*tile.pattern, sep = "\n")
                # Orient the tile so that it's pointing the correct direction based on the edge matches we found
                if len(tile.edges["bottom"]["tileMatches"]) > 0 and len(tile.edges["right"]["tileMatches"]) > 0:
                    orient = 0
                elif len(tile.edges["bottom"]["tileMatches"]) > 0 and len(tile.edges["left"]["tileMatches"]) > 0:
                    # To fit in our first corner, we'll need to rotate anticlockwise once
                    orient = -1
                elif len(tile.edges["top"]["tileMatches"]) > 0 and len(tile.edges["left"]["tileMatches"]) > 0:
                    # To fit in our first corner, we'll need to rotate clockwise twice
                    orient = 2
                elif len(tile.edges["top"]["tileMatches"]) > 0 and len(tile.edges["right"]["tileMatches"]) > 0:
                    # To fit in our first corner, we'll need to rotate clockwise once
                    orient = 1
                print("I need to orient: %d" % (orient))
                self.addTile(0,0,tile,orient,0)
                tiles.remove(tile)
                calc.remove(calc[0])
                break

        self.printTileNumberMap()    
        
    def findCorners(self, tiles):
        calc = []
        for tile in tiles:
            thisCount = tile.countTotalMatches()
            print("Tile %d has %d matches" % (tile.number, thisCount))
            if thisCount == 2:
                calc.append(tile.number)
        return calc
    
    def determineOrientation(self, dirToLook, previousTile, tile):
        orient = 0
        if dirToLook == "down":
            if previousTile.number in [abs(x) for x in tile.edges["bottom"]["tileMatches"]]:
                orient = 2
            elif previousTile.number in [abs(x) for x in tile.edges["top"]["tileMatches"]]:
                orient = 0
            elif previousTile.number in [abs(x) for x in tile.edges["right"]["tileMatches"]]:
                orient = -1
            elif previousTile.number in [abs(x) for x in tile.edges["left"]["tileMatches"]]:
                orient = 1
        else:
            if previousTile.number in [abs(x) for x in tile.edges["bottom"]["tileMatches"]]:
                orient = 1
            elif previousTile.number in [abs(x) for x in tile.edges["top"]["tileMatches"]]:
                orient = -1
            elif previousTile.number in [abs(x) for x in tile.edges["right"]["tileMatches"]]:
                orient = 2
            elif previousTile.number in [abs(x) for x in tile.edges["left"]["tileMatches"]]:
                orient = 0
        
        return orient
    
    def determineFlip(self, dirToLook, nextTile):
        flipAxis = 0
        if nextTile < 0:
            if dirToLook == "down":
                print("We need to flip left-right: %d" % (nextTile))
                flipAxis = 1
            if dirToLook == "right":
                print("We need to flip top-bottom: %d" % (nextTile))
                flipAxis = 2

            nextTile = -nextTile
        return flipAxis, nextTile
    
    def placeTiles(self, calc, tiles):
        nextTile = self.image[0][0].edges["right"]["tileMatches"][0]
        previousTile = self.image[0][0]
        dirToLook = "right"
        
        orient = 0
        locX = 1
        locY = 0
        count = len(tiles)
        while count > 0:
            print("%s] looking in %s" % (str(nextTile), str([t.number for t in tiles])))
            for tile in tiles:
                if tile.number == abs(nextTile):
                    # Now, we need to find how the two tiles connect
                    orient = self.determineOrientation(dirToLook, previousTile, tile)
                    flipAxis, nextTile = self.determineFlip(dirToLook, nextTile)
                    
                    self.addTile(locX, locY, tile, orient, flipAxis)
                    count -= 1
                    previousTile = self.image[locY][locX]
                    tiles.remove(tile)
                          
                    locX += 1
                    if locX >= self.width:
                        locX = 0
                        locY += 1
                        previousTile = self.image[locY-1][locX]
                        dirToLook = "down"
                        
                        if locY >= self.height:
                            # We've been through the entire grid...we must be done
                            count = -1
                        else:
                            nextTile = self.image[locY-1][locX].edges["bottom"]["tileMatches"][0]
                    else:
                        dirToLook = "right"
                        nextTile = self.image[locY][locX-1].edges["right"]["tileMatches"][0]
                    break
            
            self.printTileNumberMap()   


tileString = openFile("day20test.txt")
tiles = parseInput(tileString)
    
# Now, we need to find matches.  The patterns can be compared between tiles
for tile in tiles:
    for testTile in tiles:
        tile.checkMatch(testTile) 


# Now, the corners should only have two matches
# I'm cheating a bit because I'm not matching the entire image
# But this is the easiest way to find the corners
mapSize = int(math.sqrt(len(tiles)))
testMap = Map(mapSize,mapSize)
calc = testMap.findCorners(tiles)

# THis is enough to get the answer for part 1
math.prod(calc)

# For part 2, we need to assemble the image.

# First, we can try to work out which tiles go in the corners...
# Get the first corner we found. It doesn't matter which is first really. 
# This will give us a starting point...
testMap.placeFirstCorner(calc, tiles)


# Now, we can setup a loop to go from tile to tile and fit them in
testMap.placeTiles(calc, tiles)

print(testMap.image[0][0].edges)
print(*testMap.image[0][0].pattern, sep="\n")
print(testMap.image[0][1].edges)
print(*testMap.image[0][1].pattern, sep="\n")
print(testMap.image[0][2].edges)
print(*testMap.image[0][2].pattern, sep="\n")

# Using Real Data

tileString = openFile("day20.txt")
tiles = parseInput(tileString)

for tile in tiles:
    for testTile in tiles:
        tile.checkMatch(testTile)
        
calc = []
for tile in tiles:
    thisCount = tile.countTotalMatches()
    print("Tile %d has %d matches" % (tile.number, thisCount))
    print(tile.edges)
    if thisCount == 2:
        calc.append(tile.number)


print(math.prod(calc))

mapSize = int(math.sqrt(len(tiles)))
realMap = Map(mapSize,mapSize)
realMap.placeFirstCorner(calc, tiles)
realMap.placeTiles(calc, tiles)

print(realMap.image[0][0].number)
print(realMap.image[0][0].edges)
print(*np.array(realMap.image[0][0].pattern),sep="\n")


print(realMap.image[0][1].number)
print(realMap.image[0][1].edges)
print(*np.array(realMap.image[0][1].pattern),sep="\n")




