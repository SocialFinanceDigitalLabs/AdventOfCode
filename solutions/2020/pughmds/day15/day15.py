#!/usr/bin/env python
# coding: utf-8

import cProfile

test0 = {'values': [0,3,6], 'expectedAnswer': 436, 'expectedAnswer2': 175594}
test1 = {'values': [1,3,2], 'expectedAnswer': 1, 'expectedAnswer2': 2578}
test2 = {'values': [2,1,3], 'expectedAnswer': 10, 'expectedAnswer2': 3544142}
test3 = {'values': [1,2,3], 'expectedAnswer': 27, 'expectedAnswer2': 261214}
test4 = {'values': [2,3,1], 'expectedAnswer': 78, 'expectedAnswer2': 6895259}
test5 = {'values': [3,2,1], 'expectedAnswer': 438, 'expectedAnswer2': 18}
test6 = {'values': [3,1,2], 'expectedAnswer': 1836, 'expectedAnswer2': 362}

actualInput = {'values': [1,0,16,5,17,4]}


def runRules(values, maxAnswer):
    # This was my original solution, but didn't work for larger numbers
    # And isn't very memory efficient and was unable to complete the part 2
    # task in any reasonable time.
    gameValues = []
    for step in range(maxAnswer+1):
        if step < len(values):
            gameValues.append(values[step])
        else:
            lastValue = gameValues[-1]
            if lastValue in gameValues[:-1]:
                # Work out if the number has never been mentioned before
                # if it has, count times since last spoken
                lastIndex = gameValues[::-1][1:].index(lastValue)
                gameValues.append(lastIndex+1)
            else:
                # if it hasn't, this number is 0
                gameValues.append(0)   
    return gameValues    

def runRulesV2(values, maxAnswer):
    # This is my second solution which is a bit better as it doesn't store
    # ALL the instances of the numbers...only the most recent in a dictionary
    # I'm sure there are more efficeint ways to do this as this takes about 
    # a minute to complete on the 30 million part 2 task
    gameValues = {}
    lastValue = 0
    for step in range(maxAnswer):
        if step < len(values):
            # Loop over the original numbers
            gameValues[values[step]] = [step]
            lastValue = values[step]
        else:
            if len(gameValues[lastValue]) == 1:
                # if the last number appeared for the first time
                diff = 0
            else:
                # Otherwise, we need to take the 'age'
                diff = gameValues[lastValue][1] - gameValues[lastValue][0] 
            
            # Now we need to store the value found, 
            # Making sure to check if the value already exists
            if diff in gameValues.keys():
                if len(gameValues[diff]) > 1:
                    gameValues[diff] = gameValues[diff][1:]
                gameValues[diff].append(step)
            else:
                gameValues[diff] = [step]
            lastValue = diff
    return lastValue 

def runRulesV3(values, maxAnswer):
    # Made faster by switching to dictionaries, limiting use of
    # functions like "len" and "append"
    gameValues = { n : {'l': idx} for idx, n in enumerate(values) }
    lastValue = 0
    for step in range(len(values), maxAnswer):
        if "p" not in gameValues[lastValue]:
            diff = 0
        else:
            diff = gameValues[lastValue]["l"] - gameValues[lastValue]["p"]

        if diff in gameValues:
            gameValues[diff]["p"] = gameValues[diff]["l"]
            gameValues[diff]["l"] = step
        else:
            gameValues[diff] = {"l": step}
        lastValue = diff
    return lastValue 


print("---- PART 1 ------------")
print("Solution V1")
# Testing Version 1 Solution
ans = runRules(test0["values"], 2020)
if ans[2019] == test0["expectedAnswer"]:
    print("Test 0 Passes!")
else:
    print("Test 0 Failed!")

# Testing Version 2 Solution
print("Solution V2")
ans = runRulesV2(test0["values"], 2020)

if ans == test0["expectedAnswer"]:
    print("Test 0 Passes!")
else:
    print("Test 0 Failed!")

# Testing Version 3 Solution
print("Solution V3")
ans = runRulesV3(tuple(test0["values"]), 2020)
if ans == test0["expectedAnswer"]:
    print("Test 0 Passes!")
else:
    print("Test 0 Failed!")

ans = runRulesV2(test1["values"], 2020)
if ans == test1["expectedAnswer"]:
    print("Test 1 Passes!")
else:
    print("Test 1 Failed!")

ans = runRulesV2(test2["values"], 2020)
if ans == test2["expectedAnswer"]:
    print("Test 2 Passes!")
else:
    print("Test 2 Failed!")

ans = runRulesV2(test3["values"], 2020)
if ans == test3["expectedAnswer"]:
    print("Test 3 Passes!")
else:
    print("Test 3 Failed!")

ans = runRulesV2(test4["values"], 2020)
if ans == test4["expectedAnswer"]:
    print("Test 4 Passes!")
else:
    print("Test 4 Failed!")

ans = runRulesV2(test5["values"], 2020)
if ans == test5["expectedAnswer"]:
    print("Test 5 Passes!")
else:
    print("Test 5 Failed!")

ans = runRulesV2(test6["values"], 2020)
if ans == test6["expectedAnswer"]:
    print("Test 6 Passes!")
else:
    print("Test 6 Failed!")

ans = runRulesV3(actualInput["values"], 2020)
print("The result for the 2020th answer is: %d" % (ans))

print("---- PART 2 ------------")
print("Let's find out which version of the program is the fastest...")
print("Profiling Version 1 of the rules...")
cProfile.run('runRules(tuple(test0["values"]), 30000)')

print("Profiling Version 2 of the rules...")
cProfile.run('runRulesV2(tuple(test0["values"]), 30000)')

print("Profiling Version 3 of the rules...")
cProfile.run('runRulesV3(tuple(test0["values"]), 30000)')

print("Running fastest version (V3) of function on final test...")
ans = runRulesV3(actualInput["values"], 30000000)
print("The result for the 30 millionth answer is: %d" % (ans))


