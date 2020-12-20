#!/usr/bin/env python
# coding: utf-8

import re

examples = [
    {'Problem': '1 + 2 * 3 + 4 * 5 + 6', 'Answer': 71, 'Answer2': 231},
    {'Problem': '11 + 22 + 31 + 5 * 6', 'Answer': 414, 'Answer2': 414},
    {'Problem': '1 + (2 * 3) + (4 * (5 + 6))', 'Answer': 51, 'Answer2': 51},
    {'Problem': '2 * 3 + (4 * 5)', 'Answer': 26, 'Answer2': 46},
    {'Problem': '5 + (8 * 3 + 9 + 3 * 4 * 3)', 'Answer': 437, 'Answer2': 1445},
    {'Problem': '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 'Answer': 12240, 'Answer2':669060 },
    {'Problem': '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 'Answer': 13632, 'Answer2': 23340},
]

operators = ["*","-","+"]

def parseBrackets(problemString):
    bracketMap = []
    index = 0
    maxIndex = 0
    for char in problemString:
        if char == "(":
            index += 1
            if index > maxIndex:
                maxIndex += 1
        if char == ")":
            index -= 1
        bracketMap.append(index)
    if maxIndex < 0:
        maxIndex = 0
    return bracketMap, maxIndex

def locateNumber(pointer, expression, currentIndex):
    number = False
    while not number:
        pointer += 1
        if pointer >= len(expression):
            number = expression[currentIndex:pointer].strip()
        elif expression[pointer] == " ":
            continue
        elif expression[pointer].isnumeric():
            continue
        elif expression[pointer] in operators:
            number = expression[currentIndex:pointer].strip()
        elif expression[pointer] == "(":
            currentIndex += 1
            continue
        else:
            #Must be a bracket
            number = expression[currentIndex:pointer].strip()
    return number, currentIndex, pointer

def locateOperator(pointer, expression, currentIndex):
    operator = False
    while not operator:
        pointer += 1
        if expression[pointer] == " ":
            continue
        elif expression[pointer].isnumeric():
            operator = expression[currentIndex:pointer].strip()
        elif expression[pointer] in operators:
            continue
        elif expression[pointer] == "(":
            operator = expression[currentIndex:pointer].strip()
        else:
            #Must be a bracket
            operator = expression[currentIndex:pointer].strip()
    return operator, currentIndex, pointer

def calculateExpression(firstNumber, operator, secondNumber):
    if operator == "+":
        return int(firstNumber) + int(secondNumber)
    elif operator == "*":
        return int(firstNumber) * int(secondNumber)
    else:
        return "?"
    
def solveExpression(expression, printStep=False, advancedRules=False):
    # First, find the brackets
    if printStep:
        print(expression)
        
    finalAnswer = False
    
    # We want to repeat all of this:
    while not finalAnswer:
        bracketMap, idx = parseBrackets(expression)

        # Now, we work things backwards:
        try:
            firstIndex = bracketMap.index(idx)
        except:
            return False      
        
        pointer = firstIndex
        
        if expression[pointer] == "(":
            firstIndex += 1
            pointer = firstIndex
        
        if advancedRules:
            # We will want to jump ahead to any addition problem first
            # Find the next bracket ) if any
            try:
                lastIndex = expression[firstIndex:].index(")")+firstIndex
            except:
                lastIndex = None
            if not lastIndex:
                # If no bracket, substring will go to the end.
                lastIndex = len(expression) - 1

            # Move index to first instance of addition found
            try:
                firstAddition = expression[firstIndex:lastIndex].index("+") + firstIndex
            except:
                firstAddition = None
                
            if firstAddition:
                # If there's addition, we need to set the index to the number
                # value before the addition symbol
                value = re.findall(r'\d+', expression[firstIndex:firstAddition+1])[-1]
                currentIndex = expression[:firstAddition].rindex(value)
                pointer = currentIndex
                firstIndex = currentIndex
            else:
                # If none found, run normally
                currentIndex = firstIndex
        else:
            currentIndex = firstIndex
        
        firstNumber, currentIndex, pointer = locateNumber(pointer, expression, currentIndex)

        currentIndex = pointer
        operator, currentIndex, pointer = locateOperator(pointer, expression, currentIndex)

        currentIndex = pointer
        secondNumber, currentIndex, pointer = locateNumber(pointer, expression, currentIndex)

        # Work out answer:
        answer = calculateExpression(firstNumber, operator, secondNumber)        
        
        # Need different method for advanced section...
        expression = expression[:firstIndex] + str(answer) + expression[pointer:]
        
        if printStep:
            print(expression)

        expression = re.sub(
            r"\(\s*\d+\s*\)", 
            str(answer), 
            expression
        )

        if printStep:
            print(expression)
        
        
        p = re.compile('^\d+$')
        if p.match(expression):
            finalAnswer = int(expression)
    return finalAnswer
            

def openFile(filename):
    with open(filename, "r") as file:
        data = file.read()
    return data.split("\n")

for i in range(0,7):
    expression = examples[i]["Problem"]
    examples[i]["CalculatedAnswer"] = solveExpression(expression, True)
    if examples[i]["Answer"] == examples[i]["CalculatedAnswer"]:
        print("Test %d Passed!" % (i+1))

expressions = openFile("day18.txt")
answers = []
for line in expressions:
    answer = solveExpression(line)
    if answer:
        answers.append(answer)

print("The answer to part 1 is: %d" % (sum(answers)))

# Part 2
for i in range(0,7):
    print("============Test %d============" % (i+1))
    expression = examples[i]["Problem"]
    examples[i]["CalculatedAnswer"] = solveExpression(expression, False, True)
    if examples[i]["Answer2"] == examples[i]["CalculatedAnswer"]:
        print("Test %d Passed!" % (i+1))

expressions = openFile("day18.txt")
answers = []
for line in expressions:
    answer = solveExpression(line, False, True)
    if answer:
        answers.append(answer)

print("The answer to part 2 is: %d" % (sum(answers)))




