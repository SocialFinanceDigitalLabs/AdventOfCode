#!/usr/bin/env python
# coding: utf-8

'''
  I probably could do this better using binary operations,
  but this worked, and gave me the solution too, so...
'''

import itertools

testProgram1 = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''

testProgram2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''

# Implementing a structure like this will keep things
# easy to loop over

'''[
    {
        mask: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
        values: [
            {address: 8, value: 11},
            {address: 7, value: 101},
            {address: 8, value: 0},
        ]
    },
    {
        mask: '1X0110X0X110000100X01100000011101111'
        values: [
            {address: 5228, value: 409649},
            {address: 64037, value: 474625}
        ]
    },
]'''

def getBinaryString(value):
    binary = format(value, "036b")
    return binary

def parseInput(inputString):
    lines = inputString.split("\n")
    instructions = []
    instr = False
    for line in lines:
        if "mask" in line:
            # start a new object
            if instr:
                instructions.append(instr)
            instr = {
                'mask': line[line.index("=")+2:],
                'values': []
            }
        elif "mem" in line:
            # Add value to object
            instr["values"].append({
                'address': line[line.index("[")+1:line.index("]")],
                'value': line[line.index("=")+2:]
            })
    
    instructions.append(instr)        
    return instructions

def applyMask(mask, value):
    # Probably could use binary operators to do this
    newValue = []
    for idx, c in enumerate(mask):
        if c == 'X':
            newValue.append(value[idx])
        else:
            newValue.append(c)
    newValue = ''.join(newValue)
    return newValue

def applyAddressMask(mask, value):
    # Probably could use binary operators to do this
    newValue = []
    for idx, c in enumerate(mask):
        if c == 'X':
            newValue.append(c)
        else:
            newValue.append(str(int(c) | int(value[idx])))
    newValue = ''.join(newValue)
    return newValue
        
def runV1Instructions(instructionList, memory):
    for i in instructionList:
        for v in i["values"]:
            binResult = applyMask(i["mask"], getBinaryString(int(v["value"])))
            # print("input value: %d, result: %d" % (int(v["value"]), int(binResult,2)))
            memory[int(v["address"])] = int(binResult,2)

def getAddressesFromFloating(floatingAddress):
    addressList = []
    splitAddress = floatingAddress.split("X")
    
    possibleBits = list(itertools.product([0, 1], repeat=len(splitAddress)-1))
    for bit in possibleBits:
        result = splitAddress[0]
        for idx, b in enumerate(bit):    
            result += str(b)
            result += splitAddress[idx+1]
        addressList.append(result)
    return addressList

def runV2Instructions(instructionList, memory):
    for i in instructionList:
        for v in i["values"]:
            # First get the memory address as a binary string
            a = getBinaryString(int(v["address"]))
            # Next, apply the mask
            floatingAddress = applyAddressMask(i["mask"], a)
            addressList = getAddressesFromFloating(floatingAddress)
            
            # Now we need to store the found value in the list of addresses provided
            for addr in addressList:
                #print("Storing value in address: %d" % (int(addr,2)))
                memory[int(addr,2)] = int(v["value"])         
            
def openFile(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data


# Part 1 Test 1
print("Part 1 Test")
memory = {}
instructionList = parseInput(testProgram1)
runV1Instructions(instructionList, memory)
print(sum(memory.values()))

# Part 1
print("Part 1 Real")
memory = {}
instructionList = parseInput(openFile('day14.txt'))
runV1Instructions(instructionList, memory)
print(sum(memory.values()))

# Part 2 Test 1
print("Part 2 Test")
memory = {}
instructionList = parseInput(testProgram2)
runV2Instructions(instructionList, memory)
print(sum(memory.values()))

# Part 2
print("Part 2 Real")
memory = {}
instructionList = parseInput(openFile('day14.txt'))
runV2Instructions(instructionList, memory)
print(sum(memory.values()))

