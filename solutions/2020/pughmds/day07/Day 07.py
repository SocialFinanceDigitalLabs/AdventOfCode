#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import json
import sys

sys.setrecursionlimit(2500)


# In[2]:


testRules = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''


# In[3]:


class Bags:
    def __init__(self):
        self.bagRules = {}

    def addBagRule(self, ruleString):
        pattern = "^([a-z]+ [a-z]+)"
        prog = re.compile(pattern)
        result = prog.match(ruleString).group(0)
        self.bagRules[result] = {}

    def getAllBagRules(self, ruleList):
        for rule in ruleList:
            self.addBagRule(rule)
    
    def getAllContents(self, ruleList):
        for idx, rule in enumerate(ruleList):
            colourPattern = "^([a-z]+ [a-z]+)"
            colourProg = re.compile(colourPattern)
            thisColour = colourProg.match(rule).group(0)
            
            contentsPattern = r"(\d+) ([a-z]+ [a-z]+)"
            result = re.findall(contentsPattern, rule)
            for item in result:
                self.bagRules[thisColour][item[1]] = int(item[0])
    
    def containsBagType(self, bagType):
        contents = self.bagRules[bagType]
        
        if bagType in contents:
            return True
        
        foundPath = []
        for item in contents:
            try:
                if self.containsBagType(bagType):
                    foundPath.append(True)
            except Exception as e:
                print(e)
                return False
        return foundPath
        


# In[4]:


thisBagSet = Bags()
thisBagSet.getAllBagRules(testRules.split("\n"))


# In[5]:


print(thisBagSet.bagRules)


# In[6]:


thisBagSet.getAllContents(testRules.split("\n"))


# In[7]:


print(thisBagSet.bagRules)


# In[ ]:


print(thisBagSet.containsBagType("shiny gold"))


# In[ ]:




