import statistics as stats

def parseInput(input):
    inputStrings = input.split(",")
    return list(map(int, inputStrings))

def findMiddle(nums):
    '''
        The median was the best way to find the middle I could get.
        Left in a function for consistency
    '''
    return stats.median(nums)

def findMiddleV2(nums):
    '''
        Okay, I was being a bit optimistic with this version, but it passed all the tests!
        Just not the final answer as some situations need you to round down, and some up
        for this to work... Would need to study more to find out why this is the case...
    '''
    return int(stats.mean(nums)), int(round(stats.mean(nums)))

def calculateOptimalFuel(nums):
    '''
        Go through properly without estimation to get the
        real value for part 2, just to be sure...
    '''
    maxNum = max(nums)
    minNum = min(nums)
    leastFuel = None
    leastMiddle = None

    for position in range(minNum, maxNum):
        fuel = 0
        for num in nums:
            distance = abs(num - position)
            fuel += ((distance ** 2) + distance) / 2

        if not leastFuel:
            leastFuel = fuel
            leastMiddle = position
        elif fuel < leastFuel:
            leastFuel = fuel
            leastMiddle = position
    return int(leastFuel), leastMiddle

def getDistance(nums, target):
    '''
        Original way to find the Fuel usage.
        We just tally up the distance for each value
    '''
    sum = 0
    for n in nums:
        sum += abs(target - n)
    return sum

def getDistanceV2(nums, target):
    '''
        With a weighted fuel, we need to use something a bit more
        complex to add up the fuel usage
    '''
    sum = 0
    for n in nums:
        d = abs(target - n)
        ans = d * (d + 1) // 2
        sum += ans
    return sum

if __name__ == '__main__':
    # Test with sample data
    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()

    print("----PART 1-----")
    # With constant fuel cost, we can just use the median
    # which should work for most number sets (but possibly not all)
    # Thankfully, it works in this scenario, making for an easy part 1
    nums = parseInput(fileText)
    pos = findMiddle(nums)
    fuelCost = getDistance(nums, pos)
    print("Least Fuel: {} at Position {}".format(fuelCost, pos))

    print("----PART 2-----")
    # With weighted fuel, the answer is closer to the mean, so why not use it to guess?
    pos, pos2 = findMiddleV2(nums)
    fuelCost = getDistanceV2(nums, pos)
    fuelCost2 = getDistanceV2(nums, pos2)
    print("Between....")
    print("Least Fuel: {} at Position {}".format(fuelCost, pos))
    print("And....")
    print("Least Fuel: {} at Position {}".format(fuelCost2, pos2))

    print("----PART 2...FOR REALZ-----")
    # Wow! That was lucky one of those worked. I'm curious
    # How the long-way to do this would differ... Speed wise
    fuelCost, pos = calculateOptimalFuel(nums)
    print("Least Fuel: {} at Position {}".format(fuelCost, pos))

    print("--------------------")
    print("I had to try to get the hacky version down to a quick code snippet so I can tweet it. :-P")
    mid = min(int(stats.mean(nums)), int(round(stats.mean(nums))))
    f = 0
    for n in nums:
        d = abs(mid - n)
        ans = d * (d + 1) // 2
        f += ans
    print(f)