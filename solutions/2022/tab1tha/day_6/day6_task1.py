with open("input_day6.txt", "r") as f:
    stream = f.read()

def find_marker(stream, chunksize):
    for i in range(len(stream)):
        chunk = stream[i:i+chunksize]
        if len(chunk) == len(set(chunk)):
            break
    
    return i+chunksize

result1 = find_marker(stream, chunksize=4)
result2 = find_marker(stream, chunksize=14)