EXPECTED_TEST_ANSWER_PART1 = [480, 13140]
EXPECTED_TEST_ANSWER_PART2 = [
    """
##..##..................................
........................................
........................................
........................................
........................................
........................................""",
    """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""",
]

ADDX_TIME = 2
NOOP_TIME = 1


def parse_command(entry):
    """
    Parse the commands and break them into command and value
    if a value isn't present, mark it as None
    """
    if "addx" in entry:
        command, value = entry.strip().split(" ")
        return command, int(value)
    elif "noop" in entry:
        return "noop", None
    return None, None


class Processor:
    """
    This simulates the CPU for the test
    """

    def __init__(self, stop_points):
        self.cycle = 0
        self.x = 1
        self.stop_points = stop_points
        self.stop_point_scores = [0 for point in stop_points]
        self.crt_display = [
            "........................................"
            for row in range(0, int(stop_points[-1] / 40) + 1)
        ]

    def draw(self):
        """
        This function was for part 2. It takes the current cycle and sees if it
        is within range of the pixel being drawn. If so, we put a hash (#) in that
        position
        """
        x_pos = self.cycle % 40
        y_pos = int(self.cycle / 40)
        if self.x - 1 <= x_pos <= self.x + 1:
            self.crt_display[y_pos] = (
                self.crt_display[y_pos][:x_pos]
                + "#"
                + self.crt_display[y_pos][x_pos + 1 :]
            )

    def add_cycle(self, times):
        """
        The order we do things is we draw the screen,
        add a cycle, and then we check the scores only
        if the cycle is a stop point
        """
        for cycle in range(0, times):
            self.draw()
            self.cycle += 1

            if self.cycle in self.stop_points:
                idx = self.stop_points.index(self.cycle)
                self.stop_point_scores[idx] = self.cycle * self.x

    def process_command(self, command, value):
        """
        Controlling function that determines what to do based
        on the command being sent
        """
        if command == "noop":
            self.add_cycle(NOOP_TIME)
            return
        elif command == "addx":
            self.add_cycle(ADDX_TIME)
            self.x += value


def run(data):
    p = Processor([20, 60, 100, 140, 180, 220])
    for entry in data:
        command, value = parse_command(entry)
        p.process_command(command, value)
    return sum(p.stop_point_scores)


def run_p2(data):
    p = Processor([20, 60, 100, 140, 180, 220])
    for entry in data:
        command, value = parse_command(entry)
        p.process_command(command, value)
    return "\n" + "\n".join(p.crt_display)
