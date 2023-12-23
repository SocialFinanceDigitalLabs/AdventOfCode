import time
EXPECTED_TEST_ANSWER_PART1 = [4, 4, 8, 8, 4, 3]
EXPECTED_TEST_ANSWER_PART2 = [0, 0, 0, 0, 0, 0]
PIPE_CHARS = ["|", "-", "F", "7", "L", "J"]
UP_PIPES = ["|", "7", "F", "S"]
DOWN_PIPES = ["|", "J", "L", "S"]
LEFT_PIPES = ["-", "L", "F", "S"]
RIGHT_PIPES = ["-", "J", "7", "S"]

class Node:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.next_node = None

    def __str__(self):
        return f" ({self.x},{self.y})[{self.char}] "

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, x, y, char):
        new_node = Node(x, y, char)
        if self.is_empty():
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next_node:
                current_node = current_node.next_node
            current_node.next_node = new_node

    def prepend(self, x, y, char):
        new_node = Node(x, y, char)
        new_node.next_node = self.head
        self.head = new_node

    def display(self):
        elements = []
        current_node = self.head
        while current_node:
            elements.append(current_node)
            current_node = current_node.next_node
        print(" -> ".join(map(str, elements)))



class PipeMap:
    def __init__(self, map):
        self.map = [[char.strip() for char in string.strip()] for string in map]
        self.original_map = self.map.copy()
        self.remove_stray_characters()

        self.path = LinkedList()
        start = self.find_start_position()

        self.path.append(start[0], start[1], start[2])
        self.identify_loop()

    def identify_loop(self):
        self.path

    def find_start_position(self):
        position = next((i, row.index('S')) for i, row in enumerate(self.map) if 'S' in row)
        return position[1], position[0], self.map[position[0]][position[1]]

    def test_point(self, i1, j1, i2, j2, first_pipes, second_pipes):
        if i1 < 0 or i2 < 0 or j1 < 0 or j2 < 0:
            return False
        try:
            #print(f"Is surrounded by {self.map[j1][i1]} and {self.map[j2][i2]}")
            if self.map[j1][i1] in first_pipes and self.map[j2][i2] in second_pipes:
                return True
            else:
                return False
        except:
            return False

    def remove_stray_characters(self):
        # Loop over each character in the map, and make sure it connects with two other valid shapes.
        for num in range(0, len(self.map) * 5):
            for j, row in enumerate(self.map):
                for i, char in enumerate(row):
                    if char == ".":
                        continue
                    elif char == "-":
                        if not self.test_point(i-1, j, i+1, j, LEFT_PIPES, RIGHT_PIPES):
                            self.map[j][i] = "."
                    elif char == "|":
                        if not self.test_point(i, j-1, i, j+1, UP_PIPES, DOWN_PIPES):
                            self.map[j][i] = "."
                    elif char == "J":
                        if not self.test_point(i-1, j, i, j-1, LEFT_PIPES, UP_PIPES):
                            self.map[j][i] = "."
                    elif char == "F":
                        if not self.test_point(i, j+1, i+1, j, DOWN_PIPES, RIGHT_PIPES):
                            self.map[j][i] = "."
                    elif char == "7":
                        if not self.test_point(i, j+1, i-1, j, DOWN_PIPES, LEFT_PIPES):
                            self.map[j][i] = "."
                    elif char == "L":
                        if not self.test_point(i, j-1, i+1, j, UP_PIPES, RIGHT_PIPES):
                            self.map[j][i] = "."

    def get_length(self):
        total = 0
        for row in self.map:
            for char in row:
                if char in PIPE_CHARS:
                    total += 1

        return total

    def __str__(self):
        rows = len(self.map)
        cols = len(self.map[0]) if rows > 0 else 0
        result = ""
        for j in range(rows):
            for i in range(cols):
                if 0 <= j < rows and 0 <= i < len(self.map[j]):
                    result += str(self.map[j][i])
                else:
                    continue
                    #result += "\t"
            result += "\n"

        return result.strip()

def run(data):
    this_map = PipeMap(data)
    #print("--------")
    #for row in data:
    #    print(row)

    print(this_map)
    return round(this_map.get_length() / 2)


def run_p2(data):
    return 0
