def countChanges(data):
    # Probably won't need all this, but just in case...
    total = {
        "increase": 0,
        "decrease": 0,
        "same": 0
    }
    value = data[0]
    for d in data[1:]:
        if d > value:
            total["increase"] += 1
        elif d < value:
            total["decrease"] += 1
        elif d == value:
            total["same"] += 1
        value = d

    return total

def countSumChanges(data):
    # Probably won't need all this, but just in case...
    total = {
        "increase": 0,
        "decrease": 0,
        "same": 0
    }
    value = None
    for idx, d in enumerate(data[2:]):
        window = [data[idx], data[idx+1], data[idx+2]]
        if value is None:
            value = sum(window)
        result = sum(window)
        if result > value:
            total["increase"] += 1
        elif result < value:
            total["decrease"] += 1
        elif result == value:
            total["same"] += 1
        value = result

    return total


#Test with sample data
with open("input.txt", 'r') as fileStream:
    fileText = fileStream.read()
    inputStrings = fileText.split('\n')
    taskData = list(map(int, inputStrings))

if __name__ == '__main__':
    result = countChanges(taskData)
    print("----PART 1-----")
    print(result)
    print("----PART 2-----")
    result2 = countSumChanges(taskData)
    print(result2)