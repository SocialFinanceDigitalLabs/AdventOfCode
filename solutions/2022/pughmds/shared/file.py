def open_into_list(filelocation):
    with open(filelocation) as file:
        lines = [line.strip() for line in file]
    return lines
