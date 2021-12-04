def getBitCount(values):
    initial = [0] * len(values[0])

    for v in values:
        for idx, pos in enumerate(v):
            initial[idx] += int(pos)

    return initial

def getGammaRate(values):
    valueCount = len(values)
    initial = getBitCount(values)

    for idx, v in enumerate(initial):
        if v >= (valueCount / 2):
            initial[idx] = '1'
        else:
            initial[idx] = '0'

    return ''.join(initial)

def getEpsilonRate(gammaRate):
    return gammaRate.replace('1', '2').replace('0', '1').replace('2', '0')

def getPowerConsumptionFromRates(gammaRate, epsilonRate):
    g = int(gammaRate, 2)
    e = int(epsilonRate, 2)
    return g * e

def getPowerConsumption(values):
    gamma = getGammaRate(values)
    epsilon = getEpsilonRate(gamma)
    power = getPowerConsumptionFromRates(gamma, epsilon)
    return power

def getO2Rating(values):
    pointer = 0
    while len(values) > 1:
        gamma = getGammaRate(values)
        values = [x for x in values if x[pointer] == gamma[pointer]]
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return None
        else:
            pointer += 1
    return values

def getCO2Rating(values):
    pointer = 0
    while len(values) > 1:
        print(values)
        gamma = getGammaRate(values)
        epsilon = getEpsilonRate(gamma)
        print("--> {}".format(epsilon))
        values = [x for x in values if x[pointer] == epsilon[pointer]]
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return None
        else:
            pointer += 1
    return values

def getLifeSupportRating(values):
    o2rating = getO2Rating(values)
    co2rating = getCO2Rating(values)
    return int(o2rating, 2) * int(co2rating, 2)

if __name__ == '__main__':
    result = {"gamma": "", "epsilon": ""}

    with open("input.txt", 'r') as fileStream:
        fileText = fileStream.read()
        inputStrings = fileText.split('\n')


    print("----PART 1-----")
    power = getPowerConsumption(inputStrings)
    print(power)


    print("----PART 2-----")
    lifeSupport = getLifeSupportRating(inputStrings)
    print(lifeSupport)