def open_into_list(filelocation):
    print("---------------------------------")
    print(f"--> Opening file: {filelocation}")
    print("---------------------------------")
    with open(filelocation) as file:
        lines = [line.replace('\n', ' ') for line in file]
    return lines
