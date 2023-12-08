import re


def read_stat(data: str) -> list:
    lines = data.splitlines()
    times = re.compile(r"(\d+)").findall(lines[0])
    distances = re.compile(r"(\d+)").findall(lines[1])
    time = int("".join(times))
    distance = int("".join(distances))
    return time, distance


def find_midpoint(lower_bound: int, upper_bound: int) -> int:
    # can be general utils function.
    half_range = (upper_bound - lower_bound) / 2
    return round(lower_bound + half_range)


def check_win(time: int, distance: int, hold: int) -> bool:
    return (hold * (time - hold)) > distance


def compute_win_bound(time: int, distance: int, descend: bool) -> int:
    min_time, max_time = 0, time
    mid_time = find_midpoint(min_time, max_time)
    if descend:
        lower_bound, upper_bound = (min_time, mid_time)
        step = -1
    else:
        lower_bound, upper_bound = (mid_time, max_time)
        step = 1
    # Graph is a downward-facing parabola. Move from inside(apex) where all points win to outside, until failing point is found.
    while True:
        mid_bound = find_midpoint(lower_bound, upper_bound)
        # if the point we're on meets the condition but the point below it doesn't,
        if check_win(time, distance, mid_bound) and not check_win(
            time, distance, mid_bound + step
        ):
            # border value has been found.
            return mid_bound
        elif check_win(time, distance, mid_bound):
            # if midpoint is still a winning point, go lower in the graph
            if descend:
                # move more to the left hand side
                upper_bound = mid_bound
            else:
                # move towards the right hand side
                lower_bound = mid_bound
        else:
            # if it doesn't, go higher up the graph
            if descend:
                lower_bound = mid_bound
            else:
                upper_bound = mid_bound


def large_hold_options(time: int, distance: int) -> list:
    # other function times out and returns a memory error with large numbers
    min_win = compute_win_bound(time, distance, descend=True)
    max_win = compute_win_bound(time, distance, descend=False)
    return min_win, max_win


def day6_part2(filepath: str):
    with open(filepath, "r") as f:
        data = f.read()
    time, distance = read_stat(data)
    min_win, max_win = large_hold_options(time, distance)
    print(min_win, max_win)
    return (max_win - min_win) + 1


if __name__ == "__main__":
    result = day6_part2(filepath="day2\input.txt")
    print(result)
