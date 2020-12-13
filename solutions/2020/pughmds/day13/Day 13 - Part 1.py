#!/usr/bin/env python
# coding: utf-8

import math

testData = '''939
7,13,x,x,59,x,31,19'''

def parseData(dataString):
    dataString = dataString.replace("x","")
    splitData = dataString.split("\n")
    busses = splitData[1].split(",")
    busses = list(filter(None, busses))
    busses = list(map(int, busses))
    # I bet the 'x's will come up in part 2...
    arrival = int(splitData[0])
    return arrival, busses

def findNextBusTimes(arrival, num):
    lastBus = math.floor(arrival/num)
    nextBus = (lastBus + 1) * num - arrival
    return nextBus

def findNextBus(busses,nextTimes):
    nextTimeIndex = nextTimes.index(min(nextTimes)) 
    nextBus = busses[nextTimeIndex]
    return nextBus, nextTimeIndex

def getBusNumValue(arrival, busses):
    # Use modulus to find the bus that will 
    difference = [findNextBusTimes(arrival, num) for num in busses]
    print(difference)
    fastestBus, fastestBusIndex = findNextBus(busses, difference)
    print("The next bus is bus number %d which will arrive in %d minutes" % (fastestBus, difference[fastestBusIndex]))
    waitTime = difference[fastestBusIndex]
    return fastestBus, waitTime

def openFile(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

# Part 1 Test 1
print("----TEST-----")
arrival, busses = parseData(testData)
fastestBus, waitTime = getBusNumValue(arrival, busses)
print("This means the value they're looking for is %d" % (fastestBus * waitTime))

# Part 1 Real Data
print("----REAL-----")
realData = openFile("day13.txt")
arrival, busses = parseData(realData)
fastestBus, waitTime = getBusNumValue(arrival, busses)
print("This means the value they're looking for is %d" % (fastestBus * waitTime))




