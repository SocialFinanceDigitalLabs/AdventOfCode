#!/usr/bin/env python
# coding: utf-8

# In[71]:


import ast


# In[72]:


testData = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

validKeys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


# In[73]:


def parseBatchFile(text):
    passports = []
    text = text.replace(' ', '","').replace(':','":"')
    passportTextList = text.split("\n\n")
    
    for item in passportTextList:
        item = '{"' + item.replace("\n",'","') + '"}'
        item = item.replace('"",',"")
        
        itemDict=ast.literal_eval(item)
        print(itemDict)
        passports.append(itemDict)

    return passports

def getAndParseFile(filename):
    with open (filename, "r") as dataFile:
        data = dataFile.read()
        parsedData = parseBatchFile(data)
    
    return parsedData

def checkPassports(passports):
    passportCount = 0
    for item in passports:
        valid = 0
        for key in validKeys:
            if key in item.keys():
                valid += 1
        if valid == len(validKeys):
            passportCount += 1
    return passportCount


# In[74]:


# Test Run
passports = parseBatchFile(testData)


# In[75]:


passportCount = checkPassports(passports)

        
print("The number of valid passports is %d" % (passportCount))


# In[77]:


# Part 1: Real Run
passports = getAndParseFile("day4.txt")


# In[78]:


passportCount = checkPassports(passports)

        
print("The number of valid passports is %d" % (passportCount))


# In[ ]:




