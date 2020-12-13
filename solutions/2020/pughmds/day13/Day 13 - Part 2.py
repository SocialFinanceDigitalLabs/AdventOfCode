#!/usr/bin/env python
# coding: utf-8

import math
from math import gcd

testData = '''939
7,13,x,x,59,x,31,19'''
testAnswer1 = 1068781

testData2 = '''939
17,x,13,19'''
testAnswer2 = 3417

testData3 = '''939
67,7,59,61'''
testAnswer3 = 754018

testData4 = '''939
67,x,7,59,61'''
testAnswer4 = 779210

testData5 = '''939
67,7,x,59,61'''
testAnswer5 = 1261476

testData6 = '''939
1789,37,47,1889'''
testAnswer6 = 1202161486

# First, I tried to brute-force things, and it gave correct answers for all the test inputs
# The real input, however, proved to be too large.

def getLargest(numberList):
    # Return the largest number in the list
    largest = sorted(numberList)[-1]
    return largest

def parseData(dataString):
    dataString = dataString.replace("x","")
    splitData = dataString.split("\n")
    busList = splitData[1].split(",")
    busValues = list(filter(None, busList))
    busValues = list(map(int, busValues))
    # I bet the 'x's will come up in part 2...
    arrival = int(splitData[0])
    return arrival, busList, busValues

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

def bruteForceSearch(busValues, busList):
    largest = getLargest(busValues)
    counter = largest
    foundT = False
    while not foundT:
        t = counter - busList.index(str(largest))
        comboWorks = True
        for bus in busValues:
            thisBusT = t + (busList.index(str(bus)))
            if thisBusT % bus != 0:
                comboWorks = False
                break
        if comboWorks is True:
            foundT = True
        counter += largest
    return t


# part 2 Test 1
print("----TEST 1----")
arrival, busList, busValues = parseData(testData)
t = bruteForceSearch(busValues, busList)

print("The time where things all line up is %d" % (t))
if t == testAnswer1:
    print("Correct!")
else:
    print("Incorrect!")


# part 2 Test 2
print("----TEST 2----")
arrival, busList, busValues = parseData(testData2)

t = bruteForceSearch(busValues, busList)

print("The time where things all line up is %d" % (t))
if t == testAnswer2:
    print("Correct!")
else:
    print("Incorrect!")


# part 2 Test 3
print("----TEST 3----")
arrival, busList, busValues = parseData(testData3)
t = bruteForceSearch(busValues, busList)

print("The time where things all line up is %d" % (t))
if t == testAnswer3:
    print("Correct!")
else:
    print("Incorrect!")


# part 2 Test 4
print("----TEST 4----")
arrival, busList, busValues = parseData(testData4)
t = bruteForceSearch(busValues, busList)

print("The time where things all line up is %d" % (t))
if t == testAnswer4:
    print("Correct!")
else:
    print("Incorrect!")


# part 2 Test 5
print("----TEST 5----")
arrival, busList, busValues = parseData(testData5)
t = bruteForceSearch(busValues, busList)

print("The time where things all line up is %d" % (t))
if t == testAnswer5:
    print("Correct!")
else:
    print("Incorrect!")


# part 2 Test 6
print("----TEST 6----")
arrival, busList, busValues = parseData(testData6)
t = bruteForceSearch(busValues, busList)

print("The time where things all line up is %d" % (t))
if t == testAnswer6:
    print("Correct!")
else:
    print("Incorrect!")

# part 2 REAL Data
print("----REAL DATA----")
realData = openFile("day13.txt")
arrival, busList, busValues = parseData(realData)

# --------------------------------------------------
# This will NOT work as the answer is far too large!
# --------------------------------------------------
# t = bruteForceSearch(busValues, busList)


#print("The time where things all line up is %d" % (t))
#if t == testAnswer1:
#    print("Correct!")
#else:
#    print("Incorrect!")

# For the easier solution, some in the forum pointed to the Chinese remainder theorem
# This was helpful: https://www.youtube.com/watch?v=ru7mWZJlRQg

# And there was a python library for this here so I don't have to go and do 
# all the calculations described in the video: 
# https://www.geeksforgeeks.org/python-sympy-crt-method/

# Also, had a LOT of help from reading the forums to get this, so I really can't take credit:
# Interesting theory behind this. If I didn't check forums, I probably would have never figured this out
# (And I left the brute force method above running for a few hours before I even search the internet)!

from sympy.ntheory.modular import crt

realData = openFile("day13.txt")
arrival, busList, busValues = parseData(realData)

modValues = []
remainders = []

for i in range(len(busList)):
    if busList[i].isnumeric():
        modValues.append(int(busList[i]))
        remainders.append((-i) % modValues[-1])
        
answer = crt(modValues, remainders)

print("The time where things all line up is %d" % (answer[0]))





