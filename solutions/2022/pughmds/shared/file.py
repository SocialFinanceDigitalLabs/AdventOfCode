def open_into_list(filelocation):
    with open(filelocation) as file:
        lines = [line.replace('\n', ' ') for line in file]
    return lines
