#!/usr/bin/env python
# coding: utf-8

import pprint
pp = pprint.PrettyPrinter()

testData = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''

testData2 = '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9'''

def openFile(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def processInput(inputString):
    # Split into 3 sections: rules, our ticket, other tickets
    ruleSet = []
    splitString = inputString.split("ticket")
    ourTicket = splitString[1].replace("\n","").replace(" ","").replace("nearby","").replace(":","").split(",")
    rules = splitString[0].replace("your","").split("\n")
    
    for r in rules:
        r = r.strip().split(":")
        if r != ['']:
            thisRule = r[0].strip()
            ruleSet.append({"Name": thisRule, "Values": r[1].replace(" ","").split("or"), "Positions": [1]*len(ourTicket)})
        
    otherTickets = splitString[2].replace("s:","").strip().split("\n")
    for idx, t in enumerate(otherTickets):
        otherTickets[idx] = t.split(",")
    return ourTicket, ruleSet, otherTickets

def findTicketFields(otherTickets, rules):
    # We assumed at the start that all positions were valid (1) 
    # Here, we find where values don't match the rules, and switch the positions
    # to a 0 when the rule doesn't work.
    for t in otherTickets:
        for pos, value in enumerate(t):
            for ridx, r in enumerate(rules):
                results = [i for i in r["Values"] if int(i.split("-")[0]) <= int(value) and int(i.split("-")[1]) >= int(value)]
                if len(results) == 0:
                    # This number does NOT match the rules
                    rules[ridx]["Positions"][pos] = 0       
    return rules

def findErrors(otherTickets, rules):   
    errorValues = []
    errorIndices = []
    ruleCount = len(rules)
    for tIdx, t in enumerate(otherTickets):
        for pos, value in enumerate(t):
            errors = 0
            for ridx, r in enumerate(rules):
               # Check if the number in the ticket matches this rule
               # Tally up as an error if not
               ruleMatch = [i for i in r["Values"] if int(i.split("-")[0]) <= int(value) and int(i.split("-")[1]) >= int(value)]
               if len(ruleMatch) == 0:                 
                      errors += 1
                        
            # If the errors matched the rule count, then this ticket is invalid! Remove it!
            if errors == ruleCount:
                print("Removing! Ticket is invalid: %s" % (str(value)))
                errorValues.append(int(value))
                errorIndices.append(tIdx)
    return sum(errorValues), errorIndices

def removeTickets(ticketList, errorIndices):
    errorIndices.sort(reverse=True)
    for item in errorIndices:
        del ticketList[item]
    return ticketList
    
def findUniqueIndices(ticket, rules):
    count = 1
    overallRules = []
    ruleNames = []
    for r in rules:
        overallRules.append(r["Positions"]) 
        ruleNames.append(r["Name"])

    # Get the order the labels can be found based on the uniqueness of the columns
    # Thankfully this is enough for this puzzle to deduce each column in order,
    # but it won't work for ALL types of puzzles of this type
    positionOrder = [ sum(x) for x in zip(*overallRules)]
    
    # We need to keep track of the positions we've already solved
    availablePositions = list(range(1, len(ticket)+1))
    
    # Keep going until all positions are found.  Yeah, it's odd to 
    # flip values negative when I've found them. It worked for now,
    # But I'm sure there's an easier/better way to do this...
    while sum(availablePositions) != -sum(list(range(1, len(ticket)+1))):
        # Some puzzles have multiple positions with the same number of ones (e.g. the test data)
        nextCount = [i for i, x in enumerate(positionOrder) if x == count]
        for n in nextCount:
            # Loop through the rules, looking at the index we found we can solve
            for rule in rules:
                # We found a one in this position of the rule, so it is maybe the solution for this position
                if rule["Positions"][n] == 1:
                    # If this value was already tested, then continue. Shouldn't happen, but just to be safe...
                    # Otherwise, set the index as "solved" and remove the position from those available to search
                    if "Index" in rule:
                        continue
                    else:
                        rule["Index"] = n
                        availablePositions[availablePositions.index(n + 1)] *= -1
                        break
        count += 1
        
        # Safety measure to avoid infinite loops. Probably not needed, but I was nervous...
        if count > len(ticket):
            break
    return rules

def getTicketProduct(rules, findString, ticket):
    # Because Advent of code likes easy numbers to put in an input box...
    prod = 1
    for r in rules:
        if findString in r["Name"]:
            prod *= int(ticket[r["Index"]])
    return prod
            
# Test 1
print("-----------RUNNING TEST 1-----------")
ticket, rules, otherTickets = processInput(testData)
errors, errorLoc = findErrors(otherTickets, rules)
if errors == 71:
    print("Test 1 Passes!")
    
otherTickets = removeTickets(otherTickets, errorLoc)
rules = findTicketFields(otherTickets, rules)
print("Resulting rules:")
pp.pprint(rules)

# We need to work out which column goes with which index:
rules = findUniqueIndices(ticket, rules)
# There's no 'departure' for these rules, so we can't test finding a product of values
print("Using uniqueness to deduct field names:")
pp.pprint(rules)

# Test 2
print("-----------RUNNING TEST 2-----------")
ticket, rules, otherTickets = processInput(testData2)
errors, errorLoc = findErrors(otherTickets, rules)
if errors == 71:
    print("Test 1 Passes!")
    
otherTickets = removeTickets(otherTickets, errorLoc)
rules = findTicketFields(otherTickets, rules)
rules = findUniqueIndices(ticket, rules)
# There's no 'departure' for these rules, so we can't test finding a product of values
print("Using uniqueness to deduct field names:")
pp.pprint(rules)

# Real Data
print("-----------RUNNING REAL DATA RUN-----------")
realData = openFile("day16.txt")
ticket, rules, otherTickets = processInput(realData)
errors, errorLoc = findErrors(otherTickets, rules)

# Once we remove error tickets, we get the following matrix
print("Entirely for visualisation purposes, here is the result matrix:")
print(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
otherTickets = removeTickets(otherTickets, errorLoc)
rules = findTicketFields(otherTickets, rules)
for r in rules:
    print(r["Positions"], r["Name"])


rules = findUniqueIndices(ticket, rules)
result = getTicketProduct(rules, "departure", ticket)
print("Using uniqueness to deduct field names:")
pp.pprint(rules)
print("[!!] The product of all the departure field is %d" % (result))




