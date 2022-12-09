EXPECTED_TEST_ANSWER_PART1 = [1, 13, 88]
EXPECTED_TEST_ANSWER_PART2 = [1, 1, 36]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Knot_Path:
    """
    This simulates the rope. Really, I could have treated the head
    and the tail array as the same thing and saved a bit of code
    but it's written now and I don't feel like improving it at the moment.
    """
    def __init__(self, tail_size=1):
        self.head = Point(0, 0)
        self.tail = [Point(0, 0) for count in range(0, tail_size)]
        self.tail_history = [[] for count in range(0, tail_size)]

    def move_head(self, x_dir, y_dir):
        """
        Move the head and everything else follows after
        """
        self.head.x += x_dir
        self.head.y += y_dir
        # Loop over the number of tailing knots
        for idx, tail in enumerate(self.tail):
            self.adjust_tail(idx)

    def touching(self, tail_position):
        """
        This determines if two points are touching each other
        """

        # This is what I was talking about earlier when I said
        # treating the head and tails the same would have saved coding...
        if tail_position == 0:
            lead = self.head
        else:
            lead = self.tail[tail_position - 1]

        if lead.x == self.tail[tail_position].x and lead.y == self.tail[tail_position].y:
            # The two points are on top of each other
            return True
        elif (
            lead.x == self.tail[tail_position].x
            and abs(lead.y - self.tail[tail_position].y) == 1
        ):
            # The point is either 1 above or below the other
            return True
        elif (
            abs(lead.x - self.tail[tail_position].x) == 1
            and lead.y == self.tail[tail_position].y
        ):
            # The point is either 1 to the left or right of the other
            return True
        elif (
            abs(lead.x - self.tail[tail_position].x) == 1
            and abs(lead.y - self.tail[tail_position].y) == 1
        ):
            # The point is diagonal to the other
            return True
        return False

    def add_to_tail_history(self, tail_position):
        """
        Keeps track of where a tail has been on the grid
        If a point already exists in the history, then we shouldn't
        add it again.
        """
        if (
            self.tail[tail_position].x,
            self.tail[tail_position].y,
        ) not in self.tail_history[tail_position]:
            self.tail_history[tail_position].append(
                (self.tail[tail_position].x, self.tail[tail_position].y)
            )

    def move_tail(self, x_move, y_move, tail_position):
        """
        Moves the tail to the new position
        """
        self.add_to_tail_history(tail_position)
        self.tail[tail_position].x += x_move
        self.tail[tail_position].y += y_move

    def adjust_tail(self, tail_position=0):
        """
        This goes through the logic of if a tailing knot
        needs to move and if so which direction it needs
        to go.
        """
        # Could simplify by treating the head as yet another tail,
        # but I already wrote it so...
        if tail_position == 0:
            lead = self.head
        else:
            lead = self.tail[tail_position - 1]
        if not self.touching(tail_position):
            # The points aren't touching, so we need to move the tail.
            if lead.x == self.tail[tail_position].x:
                # Only the wy coordinate is different
                self.move_tail(
                    0,
                    int((self.tail[tail_position].y + lead.y) / 2)
                    - self.tail[tail_position].y,
                    tail_position,
                )
            elif lead.y == self.tail[tail_position].y:
                # Only the x coordinate is different
                self.move_tail(
                    int((self.tail[tail_position].x + lead.x) / 2)
                    - self.tail[tail_position].x,
                    0,
                    tail_position,
                )
            else:
                # We need to move diagonally...
                if (lead.x - self.tail[tail_position].x) > 0 and (
                    lead.y - self.tail[tail_position].y
                ) > 0:
                    # The head is at a greater position than the tail, so move up-right
                    self.move_tail(1, 1, tail_position)
                elif (lead.x - self.tail[tail_position].x) < 0 and (
                    lead.y - self.tail[tail_position].y
                ) < 0:
                    # The head is at a lesser position than the tail, so move down-left
                    self.move_tail(-1, -1, tail_position)
                elif (lead.x - self.tail[tail_position].x) < 0 and (
                    lead.y - self.tail[tail_position].y
                ) > 0:
                    # The head's x is less, but the y is more so move down-right
                    self.move_tail(-1, 1, tail_position)
                elif (lead.x - self.tail[tail_position].x) > 0 and (
                    lead.y - self.tail[tail_position].y
                ) < 0:
                    # The head's x is more, but the y is left, so move up-left
                    self.move_tail(1, -1, tail_position)
                    
    def print_grid(self):
        """
        Crude attempt at printing the grid and a given position of the rope at
        any given time, but i turned out not to need it so left this half-done.
        It works, but not very well...
        """
        grid = []
        for y in range(0, 210):
            grid.append([])
            for x in range(0, 210):
                grid[y].append(".")

        print(self.tail_history)
        for idx, tail in enumerate(self.tail_history):
            if len(tail) > 0:
                grid[tail[-1][1]][tail[-1][0]] = str(idx+1)

        grid[self.head.y][self.head.x] = "H"

        for row in grid:
            print("".join([point for point in row]))
        return



def process_instruction(instruction_string):
    """
    We'll track things in the "traditional" coordinate pattern
    """
    direction_str, step_count = instruction_string.strip().split(" ")
    if direction_str == "U":
        return [0, 1, int(step_count)]
    elif direction_str == "D":
        return [0, -1, int(step_count)]
    elif direction_str == "L":
        return [-1, 0, int(step_count)]
    elif direction_str == "R":
        return [1, 0, int(step_count)]
    else:
        return None


def run(data):
    knot = Knot_Path()
    for instruction in data:
        x_dir, y_dir, steps = process_instruction(instruction)
        for count in range(0, steps):
            knot.move_head(x_dir, y_dir)

    # Add 1 for the current point location...only would work
    # if the current point hasn't happened before though
    # This never happened, so left alone
    return len(knot.tail_history[-1]) + 1


def run_p2(data):
    # With part 2, there's 9 knots instead of 1, so just adjust accoringly
    knot = Knot_Path(9)
    for instruction in data:
        x_dir, y_dir, steps = process_instruction(instruction)
        for count in range(0, steps):
            knot.move_head(x_dir, y_dir)

    return len(knot.tail_history[-1]) + 1
