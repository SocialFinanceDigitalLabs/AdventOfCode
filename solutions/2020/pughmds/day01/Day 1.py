#!/usr/bin/env python
# coding: utf-8


import itertools
import math


testData = [
    1721,
    979,
    366,
    299,
    675,
    1456
]



def getCombinations(numberList, numberToChoose):
    return list(itertools.combinations(numberList, numberToChoose))

def findTarget(numbersToCheck, target):
    for group in numbersToCheck:
        if sum(group) == target:
            return math.prod(group)
    return -1

def splitInput(filename):
  inputValues = []
  with open(filename, 'r') as fileStream:
    fileText = fileStream.read()
    inputStrings = fileText.split('\n')
    inputValues = list(map(int, inputStrings))

  return inputValues



resultList = getCombinations(testData,2)
testResult = findTarget(resultList, 2020)
if testResult == 514579:
    print("Test passed!")
else:
    print("Test failed!")



inputData = splitInput('day1.txt')
print(inputData)



resultList = getCombinations(inputData,2)
testResult = findTarget(resultList, 2020)



print(testResult)



resultList = getCombinations(inputData,3)
testResult = findTarget(resultList, 2020)


print(testResult)





