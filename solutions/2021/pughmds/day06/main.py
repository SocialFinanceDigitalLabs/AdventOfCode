import numpy as np

def parseInput(input):
    inputStrings = input.split(",")
    fishList = list(map(int, inputStrings))
    return np.array(fishList, dtype=np.int64)

def step(fish):
    '''
        Tracking individual fish. This works with Small iterations,
        but gets far too big for part two unfortunately.
    '''
    fish = fish - 1
    newFish = np.sum(fish == -1)
    fish[fish == -1] = 6
    return np.hstack([np.ones(newFish)*8, fish]).astype(int)

def stepV2(fish):
    '''
        Instead of tracking individual fish, let's just
        track the stage they're at...
    '''
    spawningFish = int(fish[0])
    fish = np.roll(fish, -1)
    fish[6] += spawningFish
    return fish

if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    print("----PART 1-----")
    print("Version 1:")
    fish = parseInput(fileText)
    for i in range(0, 80):
        fish = step(fish)
    print(len(fish))

    print("Version 2:")
    fish = parseInput(fileText)

    # In the initial input, what stage is each fish at?
    fishTrack = np.array([
        len(fish[fish == 0]),
        len(fish[fish == 1]),
        len(fish[fish == 2]),
        len(fish[fish == 3]),
        len(fish[fish == 4]),
        len(fish[fish == 5]),
        len(fish[fish == 6]),
        len(fish[fish == 7]),
        len(fish[fish == 8])
    ], dtype=np.int64)

    # Step through
    for i in range(0, 80):
        fishTrack = stepV2(fishTrack)

    print(np.sum(fishTrack))

    print("----PART 2-----")
    fish = parseInput(fileText)
    fishTrack = np.array([
        len(fish[fish == 0]),
        len(fish[fish == 1]),
        len(fish[fish == 2]),
        len(fish[fish == 3]),
        len(fish[fish == 4]),
        len(fish[fish == 5]),
        len(fish[fish == 6]),
        len(fish[fish == 7]),
        len(fish[fish == 8])
    ], dtype=np.int64)
    for i in range(0, 256):
        fishTrack = stepV2(fishTrack)

    print(np.sum(fishTrack))