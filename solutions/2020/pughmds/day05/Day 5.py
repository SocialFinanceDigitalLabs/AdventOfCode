#!/usr/bin/env python
# coding: utf-8

# In[1]:


testData = [
    {"code":"FBFBBFFRLR", "seat": 357},
    {"code":"BFFFBBFRRR", "seat": 567},
    {"code":"FFFBBBFRRR", "seat": 119},
    {"code":"BBFFBBFRLL", "seat": 820}
]


# In[2]:


def openData(filename):    
    with open (filename, "r") as dataFile:
        data = dataFile.readlines()
    
    return data

class Plane:
    def __init__(self):
        self.takenSeats = []
        self.highest = 0
        self.seatList = []
        
    def showSeats(self):
        '''
            Will print out all the seats on the plane
        '''
        for seat in self.takenSeats:
            print(seat.seatNumber)
            
    def getHighestSeat(self):
        '''
            Finds the highest taken seat on the plane
        '''
        highest = 0
        for seat in self.takenSeats:
            if highest < seat.seatNumber:
                highest = seat.seatNumber
        self.highest = highest
    
    def setPlaneSeat(self, code):   
        '''
            Sets a plane's seat as occupied given a binary string
        '''
        thisSeat = Seat(code)
        thisSeat.getSeatNumber()
        self.takenSeats.append(thisSeat)
    
    def validatePlaneSeat(self, item):
        '''
            Tests a seat is calculated correctly for the test data
        '''
        thisSeat = Seat(item["code"])
        thisSeat.getSeatNumber()
        if thisSeat.seatNumber == item["seat"]:
            print("%s: Pass!" % (item["code"]))
        else:
            print("%s: Fail!" % (item["code"]))
            print("Expected %d, found %d" % (item["seat"], thisSeat.seatNumber))
            
    def findEmptySeats(self):
        '''
           This creates a sorted list of empty seats on the plane. Assumes the highest
           seat on the plane is not empty
        '''
        for seat in self.takenSeats:
            self.seatList.append(seat.seatNumber)
        emptySeats = sorted(set(range(0, self.highest)) - set(self.seatList))
        return self.findSoloSeat(emptySeats)

    def findSoloSeat(self, emptySeats):
        '''
            This should filter out any consecutively empty seats on the plane
        '''
        gaps = [[s, e] for s, e in zip(emptySeats, emptySeats[1:]) if s+1 < e]
        edges = iter(emptySeats[:1] + sum(gaps, []) + emptySeats[-1:])
        seatGroups = list(zip(edges, edges))
        for group in seatGroups:
            if group[0] == group[1]:
                return group[1]
        return 0
        


# In[3]:


class Seat:
    def __init__(self, inputData):
        self.rows = self.toBinaryString(inputData[0:7])
        self.cols = self.toBinaryString(inputData[7:])
        self.seatNumber = 0
        
    def toBinaryString(self, label):
        '''
            Changes a seat's code into a binary string
        '''
        label = label.replace("F","0").replace("L","0")
        label = label.replace("R","1").replace("B","1")
        return label
    
    def getSeatNumber(self):
        '''
            Converts a seat's row and column into a seat number
        '''
        self.seatNumber = int(self.rows,2)*8 + int(self.cols,2)
        


# In[4]:


# Run through some test data:
testPlane = Plane()
for item in testData:
    testPlane.validatePlaneSeat(item)
    testPlane.setPlaneSeat(item["code"])
    


# In[5]:


testPlane.showSeats()
print("----")
print(testPlane.getHighestSeat())


# In[6]:


# Now, we can go through the real data:
realPlane = Plane()
realData = openData("day5.txt")
for item in realData:
    realPlane.setPlaneSeat(item)
    
realPlane.getHighestSeat()


# In[8]:


mySeatNumber = realPlane.findEmptySeats()
print("My Seat Number is: %d" % (mySeatNumber))

