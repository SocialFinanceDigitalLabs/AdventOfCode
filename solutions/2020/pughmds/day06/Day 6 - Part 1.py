#!/usr/bin/env python
# coding: utf-8

testData = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


def parseData(textInput):
    # Each group is split by two newline characters
    groups = textInput.split("\n\n")
    for num, g in enumerate(groups):
        # Combine all groups into one long string of characters
        groups[num] = g.replace("\n","")
        # Turn into a set to leave only unique characters in each group
        groups[num] = set (''.join (groups[num]).replace (',', '') ) 
    return groups

def openFile(filename):
    with open (filename, "r") as dataFile:
        data = parseData(dataFile.read())
        
    return data

def countSets(groupData):
    count = 0
    for g in groupData:
        count += len(g)
    return count


#Test Run
groupData = parseData(testData)
groupCount = countSets(groupData)
print("Test Data 'yes' answers: %d " % (groupCount))


#Real Run
groupData = openFile("day6.txt")
groupCount = countSets(groupData)
print("Live Data 'yes' answers: %d " % (groupCount))

