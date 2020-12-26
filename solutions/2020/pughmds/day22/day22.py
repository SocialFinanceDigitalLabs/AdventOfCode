#!/usr/bin/env python
# coding: utf-8

testData = '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10'''

realData = '''Player 1:
42
29
12
40
47
26
11
39
41
13
8
50
44
33
5
27
10
25
17
1
28
22
6
32
35

Player 2:
19
34
38
21
43
14
23
46
16
3
36
31
37
45
30
15
49
48
24
9
2
18
4
7
20'''


def parseData(inputData):
    players = {1: [], 2: []}
    playerStrings = inputData.split("\n\n")
    for p in players.keys():
        for s in playerStrings[p-1].split("\n")[1:]:
            players[p].append(int(s))

    return players
    
    
def calculateScore(cardList):
    multiplier = len(cardList)
    score = 0
    for card in cardList:
        score += multiplier * card
        multiplier -= 1
        
    return score

def runGame(players):
    gameDone = False
    while not gameDone:
        p1card = players[1].pop(0)
        p2card = players[2].pop(0)
        if p1card > p2card:
            players[1].append(p1card)
            players[1].append(p2card)
        else:
            players[2].append(p2card)
            players[2].append(p1card)
        if len(players[1]) == 0 or len(players[2]) == 0:
            gameDone = True
        print(players,"\n")
    return players

players = parseData(testData)
players = runGame(players)

if len(players[1]) > 0:
    print("Player 1 wins with a score of: %d" % calculateScore(players[1]))
else:
    print("Player 2 wins with a score of: %d" % calculateScore(players[2]))


players = parseData(realData)
players = runGame(players)
if len(players[1]) > 0:
    print("Player 1 wins with a score of: %d" % calculateScore(players[1]))
else:
    print("Player 2 wins with a score of: %d" % calculateScore(players[2]))
