import itertools

xValue = 5
location = 0 
testDataString = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''

testData = testDataString.split("\n")
testData = list(map(int, testData))
print(testData[location+xValue])
print(testData[location:location+xValue])

def findAllowedValues(numberList):
    allowedValues = []
    combinations = list(itertools.combinations(numberList, 2))
    for pair in combinations:
        allowedValues.append(pair[0] + pair[1])
    return allowedValues

def loopOverList(numberList, location, xValue):
    foundIncorrectValue = False
    while not foundIncorrectValue:
        if location + xValue < len(numberList):
            allowedValues = findAllowedValues(numberList[location:location + xValue])
            if numberList[location + xValue] not in allowedValues:
                foundIncorrectValue = True
                break
            else:
                location += 1
        else:
            # Have not found any number in the list which breaks the rules
            return []
            
    return numberList[location+xValue]

def openFile(filename):
    with open (filename, "r") as dataFile:
        data = dataFile.read().strip().split("\n")
        data = list(map(int, data))
        
    return data      

def findNumberSums(numberList, incorrectValue):
    startIndex = 0
    foundSum = False
    while not foundSum:
            foundSum = True

def findNumberSums(testData, targetSum):
    foundChain = False
    currentIndex = 0
    while not foundChain:
        currentSum = 0
        endIndex = currentIndex
        currentSum += testData[currentIndex]
        while currentSum < targetSum:
            endIndex += 1
            if endIndex >= len(testData):
                return False, False
            currentSum += testData[endIndex]
        
        if currentSum == targetSum:
            return currentIndex, endIndex
        else:
            currentIndex += 1
            if currentIndex >= len(testData):
                return False, False
    return False, False       

def calculateEncryptionWeaknessSum(data, first, second):
    subList = data[first: second + 1]
    subList = sorted(subList)

    encryptionWeakness = subList[0] + subList[-1]
    return encryptionWeakness

# Try with Part 1 Test Data
result = loopOverList(testData, location, xValue)
print("The Incorrect Test Value is %d" % (result))

# Part 2 Test: Find the number sums to make incorrect value
xValue = 5
location = 0 
first, second = findNumberSums(testData, result)
result = calculateEncryptionWeaknessSum(testData, first, second)
print("The Test Encryption Weakness Result is %d" % (result))

# Part 1 Actual Run
xValue = 25
location = 0
data = openFile("day09.txt")
result = loopOverList(data, location, xValue)
print("The Incorrect Actual Value is %d" % (result))

# Part 2 Actual Run
xValue = 25
location = 0 
first, second = findNumberSums(data, result)
result = calculateEncryptionWeaknessSum(data, first, second)
print("The Actual Encryption Weakness Result is %d" % (result))