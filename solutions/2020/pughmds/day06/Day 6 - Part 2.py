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
    # Each group is split by two newlines
    groups = textInput.split("\n\n")
    for num, g in enumerate(groups):
        groups[num] = g.split("\n") # Split group's answers into a list
        groups[num] = list(filter(None, groups[num])) # Get rid of any stray empty elements
        
        if len(groups[num]) > 1:
            # If there's more than one person in the group, we find the intersection of the sets of characters
            for idx, item in enumerate(groups[num]):
                groups[num][idx] = set(item)
            groups[num] = set(''.join(sorted(set.intersection(*groups[num]))))
        else:
            # Otherwise, we just turn the one answer into a set of characters
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
print("Test Data: whole-group 'yes' answers: %d " % (groupCount))


#Real Run
groupData = openFile("day6.txt")
groupCount = countSets(groupData)
print("Live Data: whole-group 'yes' answers: %d " % (groupCount))




