'''
    0 = abcefg  = length of 6
    1 = cf      = length of 2
    2 = acdeg   = length of 5
    3 = acdfg   = length of 5
    4 = bcdf    = length of 4
    5 = abdfg   = length of 5
    6 = abdefg  = length of 6
    7 = acf     = length of 3
    8 = abcdefg = length of 7
    9 = abcdfg  = length of 6
'''

def parseInput(inputText):
    # Parse the input string into outputs and signals
    signalPatterns = []
    outputValues = []
    inputLines = inputText.strip().split("\n")
    for i in inputLines:
        a, b = i.strip().split("|")
        signalPatterns.append(a.strip().split(" "))
        outputValues.append(b.strip().split(" "))

    return signalPatterns, outputValues

def countUnique(output):
    # Part 1 solution
    count = 0
    for item in output:
        if len(item) in [2,3,4,7]:
            count += 1
    return count

def determineValue(codeList):
    '''
    This is very convoluted, but goes step by step using what we know to determine the next.
    THere's probably a quicker way to do this, but it works, so...
    '''
    codeMapping = ["", "","","","","","","","",""]
    for item in codeList:
        if len(item) == 2:
            codeMapping[1] = item
        elif len(item) == 3:
            codeMapping[7] = item
        elif len(item) == 4:
            codeMapping[4] = item
        elif len(item) == 7:
            codeMapping[8] = item

    len5list = []
    len6list = []
    for item in codeList:
        if len(item) == 5:
            len5list.append(item)
        if len(item) == 6:
            len6list.append(item)

    # Let's figure out 9
    for item in len6list:
        if len(list(set(codeMapping[4]) & set(item))) == 4:
            codeMapping[9] = item

    # Working out the difference between 8 and 9 should give us the value of the bottom-left bar
    tmp = list(set(codeMapping[9]))
    bottomLeftBar = [i for i in codeMapping[8] if i not in tmp]

    # We can now find 2 as it's the only length-5 number with a bottom-left bar
    for item in len5list:
        if bottomLeftBar[0] in item:
            codeMapping[2] = item

    # Let's find 3 as it's the only one that 7 can fit inside of
    for item in len5list:
        if codeMapping[7][0] in item and codeMapping[7][1] in item and codeMapping[7][2] in item:
            codeMapping[3] = item

    # The odd one out here is the 5
    for item in len5list:
        if item not in codeMapping:
            codeMapping[5] = item

    # Let's find 0, as it's the only one that 7 can fit inside of except the 9 (which we already know)
    for item in len6list:
        if codeMapping[7][0] in item and codeMapping[7][1] in item and codeMapping[7][2] in item and item != codeMapping[9]:
            codeMapping[0] = item

    # Finally, the last is 6
    for item in len6list:
        if item not in codeMapping:
            codeMapping[6] = item

    return codeMapping

def decode(codeMap, output):
    '''
        Take an output and match it to the codeMap to return a character (number)
    '''
    result = False
    for idx, code in enumerate(codeMap):
        if sorted(code) == sorted(output):
            result = str(idx)
    return result

def run(inputText):
    '''
    Run the decoding process
    '''
    signalPatterns, outputValues = parseInput(inputText)
    result = determineValue(signalPatterns[0])
    valueSum = 0
    for idx, signal in enumerate(signalPatterns):
        translatedSignal = determineValue(signal)
        valueMap = []
        for output in outputValues[idx]:
            value = decode(translatedSignal, output)
            valueMap.append(value)
        valueSum += int(''.join(valueMap))
    return valueSum


if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    print("----PART 1-----")
    signalPatterns, outputValues = parseInput(fileText)
    total = 0
    for output in outputValues:
        total += countUnique(output)
    print(total)

    print("----PART 2-----")
    result = run(fileText)
    print(result)