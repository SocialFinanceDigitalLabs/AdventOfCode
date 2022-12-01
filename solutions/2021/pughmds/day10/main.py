points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

part2points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

openChars = ["(","[","{","<"]
closeChars = [")","]","}",">"]

def parseRow(line):
    '''
    Returns if it finds an error character, returns True otherwise
    (to say that there isn't any errors)
    '''
    level = 0
    lastOpen = [line[0]]
    for char in line[1:]:
        if char in openChars:
            level += 1
            lastOpen.append(char)
        if char in closeChars:
            level -= 1
            # Check to see if char matches what it should.
            if closeChars.index(char) == openChars.index(lastOpen[-1]):
                lastOpen.pop()
                continue
            else:
                # Error
                return char
    return True

def parseRowV2(line):
    '''
    Only needed to slightly modify the part 1 solution so that it returns the odd brackets
    that need closing, and False otherwise
    '''
    level = 0
    lastOpen = [line[0]]
    for char in line[1:]:
        if char in openChars:
            level += 1
            lastOpen.append(char)
        if char in closeChars:
            level -= 1
            # Check to see if char matches what it should.
            if closeChars.index(char) == openChars.index(lastOpen[-1]):
                lastOpen.pop()
                continue
            else:
                # Error
                return False
    return lastOpen

def findClosingBrackets(brackets):
    '''
    To get this, we need to just reverse the list we found
    and then replace each with the equivalent closing
    bracket
    '''
    openBrackets = []
    for char in brackets[::-1]:
        openBrackets.append(closeChars[openChars.index(char)])
    return openBrackets

def calculateScore(items):
    score = 0
    for item in items:
        if item in points:
            score += points[item]
    return score

def calculateP2Score(brackets):
    score = 0
    for b in brackets:
        score = score * 5 + part2points[b]

    return score


if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    print("----PART 1-----")
    code = fileText.split("\n")
    results = []
    for row in code:
        results.append(parseRow(row))

    print(calculateScore(results))

    print("----PART 2-----")
    results = []
    for row in code:
        results.append(parseRowV2(row))

    scores = []
    for row in results:
        if row:
            closeBrackets = findClosingBrackets(row)
            scores.append(calculateP2Score(closeBrackets))

    scores = sorted(scores)
    print(scores[int(len(scores) / 2)])