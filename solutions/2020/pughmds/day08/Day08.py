#!/usr/bin/env python
# coding: utf-8

import copy

testInstructionString = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''  


def parseInstructions(instructionsString):
    instructions = []
    for i in instructionsString.split("\n"):
        thisInstruction = {}
        thisInstruction["command"] = i.split(" ")[0]
        thisInstruction["value"] = int(i.split(" ")[1])
        thisInstruction["executionTimes"] = 0
        instructions.append(thisInstruction)
    return instructions

def runProgramUntilLoop(instructions, loopCount):
    pointer = 0
    accumulator = 0
    finished = False
    while not finished:
        instructions[pointer]["executionTimes"] += 1
        if instructions[pointer]["executionTimes"] > loopCount:
            finished = True
        else:
            if instructions[pointer]["command"] == "nop":
                pointer += 1
            elif instructions[pointer]["command"] == "acc":
                accumulator += instructions[pointer]["value"]
                pointer += 1
            elif instructions[pointer]["command"] == "jmp":
                pointer += instructions[pointer]["value"]
    return accumulator

def runProgramUntilEnd(instructions, maxExecutions):
    pointer = 0
    accumulator = 0
    finished = False
    while not finished:
        if pointer >= len(instructions):
            finished = True
            return accumulator
        instructions[pointer]["executionTimes"] += 1
        if instructions[pointer]["executionTimes"] > maxExecutions:
            # This is stuck in an infinite loop. Stop!
            finished = True
            return False
        else:
            if instructions[pointer]["command"] == "nop":
                pointer += 1
            elif instructions[pointer]["command"] == "acc":
                accumulator += instructions[pointer]["value"]
                pointer += 1
            elif instructions[pointer]["command"] == "jmp":
                pointer += instructions[pointer]["value"]
    return accumulator

def resetLoopCount(instructions):
    for i in instructions:
        i["executionTimes"] = 0

def findCorruptInstructionIndex(instructions, loopCount):
    foundIndex = False
    swapIndex = 0
    while not foundIndex:
        #print("Testing Index: %d" % (swapIndex))
        testInstructions = copy.deepcopy(instructions)
        
        # We want to swap this instruction to see if it fixes things
        if testInstructions[swapIndex]["command"] == "jmp":
            #print("Swapping a JMP for a NOP...")
            testInstructions[swapIndex]["command"] = "nop"
        elif testInstructions[swapIndex]["command"] == "nop":
            #print("Swapping a NOP for a JMP...")
            testInstructions[swapIndex]["command"] = "jmp"
        else:
            #print("Found a command that wasn't jmp or nop: %s" % (testInstructions[swapIndex]["command"]))
            swapIndex += 1
        
        foundResult = runProgramUntilEnd(testInstructions, 5)
        if not foundResult:
            #print("Stuck in a loop still...trying the next one")
            swapIndex += 1
        else:
            #print("Found a program that fixes the issue")
            foundIndex = True
            return swapIndex, foundResult
            
        if swapIndex >= len(testInstructions):
            #print("Reached the end of the instructions with no known fix")
            foundIndex = True
            
    return swapIndex, foundResult
    
def openFile(filename):
    with open (filename, "r") as dataFile:
        data = parseInstructions(dataFile.read())
        
    return data        
            
# Part 1 Test
testInstructions = parseInstructions(testInstructionString)
index = runProgramUntilLoop(testInstructions, 1)
print("The first time the program loops is here: %d" % (index))

# Part 1 Real Run
instructions = openFile("day08.txt")
result = runProgramUntilLoop(instructions, 1)
print("The Accumulator's value is: %d" % (result))

# Part 2 Test
resetLoopCount(testInstructions)
index = findCorruptInstructionIndex(testInstructions,1)

indexToSwap, accumulator = findCorruptInstructionIndex(testInstructions, 5)
print("If you swap index %d, then the program finishes with an accumulator value of %d" % (indexToSwap, accumulator))

# Part 2 Real
resetLoopCount(instructions)
index = findCorruptInstructionIndex(instructions,1)

indexToSwap, accumulator = findCorruptInstructionIndex(instructions, 5)
print("If you swap index %d, then the program finishes with an accumulator value of %d" % (indexToSwap, accumulator))



