#!/usr/bin/env python
# coding: utf-8

from functools import reduce

targetJoltage = 0

testData1 = '''16
10
15
5
1
11
7
19
6
12
4'''

testData2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''

def getDeviceRating(adapterList):
    return adapterList[-1]+3
    
def parseInput(dataString):
    dataSplit = dataString.strip().split("\n")
    data = list(map(int, dataSplit))
    data = sorted(data)
    return data

def openFile(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data


def adapterTally(tracker, value):
    # If the current adapter value is
    # within the range of adapter - 1
    # for the past adapters, we increment
    # the counter because there is another
    # potential path
    total = 0
    if value - 3 <= tracker[0][1]:
        total = tracker[0][0]
    if value - 3 <= tracker[1][1]:
        total += tracker[1][0]
    if value - 3 <= tracker[2][1]:
        total += tracker[2][0]
    
    # This shifts the values we're looking at along
    # like a sort of queue, keeping a running total 
    # on the last set of the array
    result = [
        tracker[1],
        tracker[2],
        (
            total,
            value
        )
    ]
    print(value, result)
    return result

def findCombinations(adapters):
    # Three values as the largest difference we can have is three.
    # I got the idea of using reduce for this
    # from a forum post suggestion and reading
    # this: https://realpython.com/python-reduce-function/
    startingPoint = [ (0,0),(0,0),(1,0) ]
    result = reduce(adapterTally, adapters, startingPoint )
    print(result)
    return result[-1][0]


#Part 1 Test 1
adapters = [targetJoltage] + parseInput(testData1)
rating = getDeviceRating(adapters)
adapters = adapters + [rating]
print(adapters)
differences = [j - i for i, j in list(zip(adapters, adapters[1:]))]
oneSteps = differences.count(1)
twoSteps = differences.count(2)
threeSteps = differences.count(3)
answer = oneSteps * threeSteps
print(differences)
print(answer)


findCombinations(adapters[1:-1])


# Part 1 Test 2
adapters = [targetJoltage] + parseInput(testData2)
rating = getDeviceRating(adapters)
adapters = adapters + [rating]
print(adapters)
differences = [j - i for i, j in list(zip(adapters, adapters[1:]))]
oneSteps = differences.count(1)
twoSteps = differences.count(2)
threeSteps = differences.count(3)
answer = oneSteps * threeSteps
print("Using all the adapters we get 1step * 3steps = %d " % (answer))
combinations = findCombinations(adapters[1:-1])
print("The numbber of adapter combinations is %d" % (combinations))


# Real Part 1
adapters = [targetJoltage] + parseInput(openFile("day10.txt"))
rating = getDeviceRating(adapters)
adapters = adapters + [rating]
print(adapters)
differences = [j - i for i, j in list(zip(adapters, adapters[1:]))]
oneSteps = differences.count(1)
twoSteps = differences.count(2)
threeSteps = differences.count(3)
answer = oneSteps * threeSteps
print(oneSteps)
print(threeSteps)
print(answer)


# real part 2
print(findCombinations(adapters[1:-1]))




