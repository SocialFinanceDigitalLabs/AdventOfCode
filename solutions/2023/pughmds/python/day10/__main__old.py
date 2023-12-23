'''
Original attempt where I was overthinking it...
'''
import time
EXPECTED_TEST_ANSWER_PART1 = [4, 4, 8, 8]
EXPECTED_TEST_ANSWER_PART2 = [0, 0, 0, 0]
PIPE_CHARS = ["|", "-", "F", "7", "L", "J"]
UP_PIPES = ["|", "7", "F"]
DOWN_PIPES = ["|", "J", "L"]
LEFT_PIPES = ["-", "L", "F"]
RIGHT_PIPES = ["-", "J", "7"]


class Point:
    """
    No real need to make a point like this, but it may be
    useful to keep track of things...
    """
    def __init__(self, x, y, char):
        self._x = x
        self._y = y
        self._char = char
        self._up = False
        self._down = False
        self._left = False
        self._right = False
        self.check_char()

    @property
    def char(self):
        return self._char

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def up(self):
        return self._up

    @property
    def down(self):
        return self._down

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


    def check_char(self):
        # It's a rule that the order should follow the Konami Code... https://en.wikipedia.org/wiki/Konami_Code
        direction_mapping = {
            "|": (True, True, False, False),
            "-": (False, False, True, True),
            "J": (True, False, True, False),
            "F": (False, True, False, True),
            "7": (False, True, True, False),
            "S": (True, True, True, True),
            "L": (True, False, False, True)
        }

        self._up, self._down, self._left, self._right = direction_mapping.get(self.char, (False, False, False, False))

    def __str__(self):
        return f"({self._x}, {self._y}): [U:{self._up}, D:{self._down}, L:{self._left}, R:{self._right}] --> '{self._char}'"


class PipeMap:
    def __init__(self, map):
        self.map = map
        self.start_pos = self.find_start_position()
        self.pipe_path = self.get_pipe_path()

    def find_start_position(self):
        position = next((i, row.index('S')) for i, row in enumerate(self.map) if 'S' in row)
        return Point(position[1], position[0], self.map[position[0]][position[1]])

    def get_surrounding_points(self, this_point):
        surrounding = [0, 0, 0, 0]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for i, (dy, dx) in enumerate(directions):
            try:
                surrounding[i] = self.map[this_point.y + dy][this_point.x + dx]
                if surrounding[i] == ' ':
                    surrounding[i] = '.'
            except IndexError:
                surrounding[i] = "."

        # Now, let's narrow things so that we only are shown points we can get to
        if not this_point.up:
            surrounding[0] = "."
        if not this_point.down:
            surrounding[1] = "."
        if not this_point.left:
            surrounding[2] = "."
        if not this_point.right:
            surrounding[3] = "."

        return surrounding

    def get_pipe_path(self):
        path = []
        steps = 0

        print("------------Using this Map------------")
        print(self.map)

        current_location = self.start_pos
        path.append(self.start_pos)
        came_from_direction = False
        loop_connected = False
        while not loop_connected:
            # First, have a look around us based on the point's perspective
            surrounding = self.get_surrounding_points(current_location)
            next_pipe = -1
            # Now, we need to turn off the direction we came from
            if came_from_direction >= 0:
                print(f"Let's disable where we come from: {came_from_direction}")
                surrounding[came_from_direction] = "."

            # Next, we need to check if there are more than two paths leading from the point we're at.
            possible_path_count = len(surrounding) - surrounding.count(".")
            print(surrounding)
            print(f"At step {steps} on char {current_location.char} ({current_location.x},{current_location.y}), I found {possible_path_count} possible paths to follow.")
            # If there are only one or two paths, we can just follow and move to the next stage.
            if possible_path_count > 2:
                # This may happen in the starting position, but maybe others...
                print("Unsure which path to follow...")
                break
            else:
                # Follow the first route we can
                for char in PIPE_CHARS:
                    try:
                        next_pipe = surrounding.index(char)
                        break
                    except:
                        continue
                print(f"Following: {surrounding[next_pipe]}")
                time.sleep(0.5)
                # Determine which way that character wants us to go, and if the character is a valid path
                # Create and store this point
                if "S" in surrounding:
                    # We need to trigger the end
                    print("We see the Starting point!")
                    start_location = surrounding.index("S")
                    if start_location == 0 and current_location.char in UP_PIPES:
                        loop_connected = True
                    elif start_location == 1 and current_location.char in DOWN_PIPES:
                        loop_connected = True
                    elif start_location == 2 and current_location.char in LEFT_PIPES:
                        loop_connected = True
                    elif start_location == 3 and current_location.char in RIGHT_PIPES:
                        loop_connected = True
                    else:
                        print(f"I'm not sure what to do: {char} has surrounding chars {surrounding}")
                elif next_pipe == 0 and surrounding[next_pipe] in UP_PIPES:
                    current_location = Point(current_location.x, current_location.y - 1, surrounding[next_pipe])
                    print(f"Going Up to {surrounding[next_pipe]}!")
                    came_from_direction = 1
                    path.append(current_location)
                elif next_pipe == 1 and surrounding[next_pipe] in DOWN_PIPES:
                    current_location = Point(current_location.x, current_location.y + 1, surrounding[next_pipe])
                    print(f"Going Down to {surrounding[next_pipe]}!")
                    came_from_direction = 0
                    path.append(current_location)
                elif next_pipe == 2 and surrounding[next_pipe] in LEFT_PIPES:
                    current_location = Point(current_location.x - 1, current_location.y, surrounding[next_pipe])
                    print(f"Going Left to {surrounding[next_pipe]}!")
                    came_from_direction = 3
                    path.append(current_location)
                elif next_pipe == 3 and surrounding[next_pipe] in RIGHT_PIPES:
                    current_location = Point(current_location.x + 1, current_location.y - 1, surrounding[next_pipe])
                    print(f"Going Right to {surrounding[next_pipe]}!")
                    came_from_direction = 2
                    path.append(current_location)

            steps += 1
        return path

    def __str__(self):
        rows = len(self.map)
        cols = len(self.map[0]) if rows > 0 else 0
        result = ""
        for i in range(rows):
            for j in range(cols):
                if 0 <= i < rows and 0 <= j < len(self.map[i]):
                    result += str(self.map[i][j]) + "\t"
                else:
                    result += "\t"
            result += "\n"

        return result.strip()

def run(data):
    this_map = PipeMap(data)

    print(this_map)
    return len(this_map.pipe_path)


def run_p2(data):
    return 0
