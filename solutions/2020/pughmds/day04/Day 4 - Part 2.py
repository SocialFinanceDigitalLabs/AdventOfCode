#!/usr/bin/env python
# coding: utf-8

# In[95]:


import ast
from schema import Schema, And, Use, Optional, SchemaError
import re


# In[96]:


passportSchema = Schema({
    'byr': And(Use(int), lambda n: 1920 <= n <= 2002),
    'iyr': And(Use(int), lambda n: 2010 <= n <= 2020),
    'eyr': And(Use(int), lambda n: 2020 <= n <= 2030),
    'hgt': And(Use(str), lambda n: validateHeight(n)),
    'hcl': And(Use(str), lambda n: validateHexColour(n)),
    'ecl': And(Use(str), lambda n: n in ('amb','blu','brn','gry','grn','hzl','oth')),
    'pid': And(Use(str), lambda n: validatePid(n)),
    Optional('cid'): And(Use(str))
})


# In[97]:


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

invalidTestData = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

validTestData = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

validKeys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


# In[98]:


def validateHeight(h):
    match = re.match(r"([0-9]+)([a-z]+)", h, re.I)
    if match:
        items = match.groups()
        if items[1] == 'in':
            if int(items[0]) >= 59 and int(items[0]) <= 76:
                return True
        elif items[1] == 'cm':
            if int(items[0]) >= 150 and int(items[0]) <= 193:
                return True
    return False

def validateHexColour(c):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){2}$', c)
    if match:
        return True
    return False

def validatePid(p):
    match = re.search(r'^(?:[0-9]{9})$', p)
    if match:
        return True
        
    return False

def parseBatchFile(text):
    passports = []
    text = text.replace(' ', '","').replace(':','":"')
    passportTextList = text.split("\n\n")
    
    for item in passportTextList:
        item = '{"' + item.replace("\n",'","') + '"}'
        item = item.replace('"",',"")
        
        itemDict=ast.literal_eval(item.replace(',""',""))
        print(itemDict)
        passports.append(itemDict)

    return passports

def getAndParseFile(filename):
    with open (filename, "r") as dataFile:
        data = dataFile.read()
        parsedData = parseBatchFile(data)
    
    return parsedData

def validatePassports(passports):
    valid = []
    for item in passports:
        try:
            res = passportSchema.validate(item)
            valid.append(item)
        except SchemaError as e:
            continue
        
    return valid


# In[99]:


# Test Run
passports = parseBatchFile(testData)
valid = validatePassports(passports)
        
print("The number of valid passports is: %d" % len(valid))


# In[100]:


# Test Run of Invalid Passports
passports = parseBatchFile(invalidTestData)
valid = validatePassports(passports)
        
print("The number of valid passports is: %d" % len(valid))


# In[101]:


# Test Run of Valid Passports
passports = parseBatchFile(validTestData)
valid = validatePassports(passports)
        
print("The number of valid passports is: %d" % len(valid))


# In[102]:


# Part 1: Real Run
passports = getAndParseFile("day4.txt")


# In[103]:


#checkedPassports = checkPassports(passports)
valid = validatePassports(passports)
        
print("The number of valid passports is: %d" % len(valid))


# In[ ]:




