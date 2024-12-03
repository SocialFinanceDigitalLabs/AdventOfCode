def open_file(file_path):
    with open(file_path) as file:
        lines = [line.replace("\n", " ") for line in file]
    return lines
