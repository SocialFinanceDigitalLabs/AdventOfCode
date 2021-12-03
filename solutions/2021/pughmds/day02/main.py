
def parseInput(inputStrings):
    commands = []
    for i in inputStrings:
        c = {}
        tmp = i.split(" ")
        c["command"] = tmp[0]
        c["distance"] = int(tmp[1])
        commands.append(c)
    return commands

def traceDirectionsV1(commands, position):
    for c in commands:
        if c["command"] == "down":
            position["depth"] += c["distance"]
        elif c["command"] == "forward":
            position["horizontal"] += c["distance"]
        elif c["command"] == "up":
            position["depth"] -= c["distance"]
    return position

def traceDirectionsV2(commands, position):
    for c in commands:
        if c["command"] == "down":
            position["aim"] += c["distance"]
        elif c["command"] == "forward":
            position["horizontal"] += c["distance"]
            position["depth"] += (c["distance"] * position["aim"])
        elif c["command"] == "up":
            position["aim"] -= c["distance"]
    return position

if __name__ == '__main__':
    position = {"horizontal": 0, "depth": 0, "aim": 0}
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()
        inputStrings = fileText.split('\n')

    commands = parseInput(inputStrings)
    print("----PART 1-----")
    position = traceDirectionsV1(commands, position)
    print(position)
    print("Check: {}".format(position["horizontal"] * position["depth"]))


    print("----PART 2-----")
    position = {"horizontal": 0, "depth": 0, "aim": 0}
    position = traceDirectionsV2(commands, position)
    print(position)
    print("Check: {}".format(position["horizontal"] * position["depth"]))