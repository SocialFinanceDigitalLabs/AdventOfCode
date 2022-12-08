from functools import reduce

EXPECTED_TEST_ANSWER_PART1 = [21]
EXPECTED_TEST_ANSWER_PART2 = [8]


class Forest:
    """Stores the forest we're looking at in a grid"""

    def __init__(self):
        self.grid = []

    @staticmethod
    def set_visibility(group, status=True):
        """
        Sets all trees in a given list (group)
        to be visible. Useful for the outside
        edges of the forest in part 1
        """
        for tree in group:
            tree.visible = True

    @staticmethod
    def adjust_viewing_distance(tree, line_of_sight):
        """
        Given a line of sight (up from the tree, down, etc)
        Work out how far you can see before hitting a tree
        of equal or greater height. For part 2
        """
        distance = 0
        for item in line_of_sight:
            distance += 1
            if tree.height <= item:
                break
        return distance

    @staticmethod
    def calculate_score_from_distance(tree):
        """
        Work out the score needed to submit the
        website for Part 2 (multiply all the distances)
        """
        tree.view_score = reduce(lambda x, y: x * y, tree.view_distance)

    def count_visible_trees(self):
        """
        Go through the grid and count how many trees
        are visible from the outside for Part 1
        """
        count = 0
        for row in self.grid:
            for tree in row:
                if tree.visible:
                    count += 1
        return count

    def find_view_distance(self):
        """
        Loop to go tree by tree, calculate how far you can see in
        each direction, and save the score of each tree (used for part 2)
        """
        largest_score = 0
        for yidx, row in enumerate(self.grid):
            for xidx, tree in enumerate(row):
                # Following the Konami order... Up, Down, Left, Right
                distance = [0, 0, 0, 0]

                # Could probably get rid of this and put it in the list, but
                # Flipping this list seemed easier than flipping its generation...
                # In other words, left here because I was feeling lazy...but not good
                # to leave something like this unresolved.
                left = self.get_tree_line_heights(0, yidx, xidx, yidx + 1)
                left.reverse()

                line_of_sight = [
                    self.get_tree_line_heights(xidx, yidx - 1, xidx - 1, -1),
                    self.get_tree_line_heights(
                        xidx, yidx + 1, xidx + 1, len(self.grid)
                    ),
                    left,
                    self.get_tree_line_heights(xidx + 1, yidx, len(row), yidx + 1),
                ]

                for idx, direction in enumerate(distance):
                    distance[idx] = self.adjust_viewing_distance(
                        tree, line_of_sight[idx]
                    )

                tree.view_distance = distance

                self.calculate_score_from_distance(tree)

                # Is this tree's score the largest? Keep a running check
                if tree.view_score > largest_score:
                    largest_score = tree.view_score
        return largest_score

    def find_visible_trees(self):
        """
        Part 1 main function to look at each tree and work out
        if it is visible from the outside of the forest
        """
        # First, outside edges are all visible
        self.set_visibility(self.grid[0], True)
        self.set_visibility(self.grid[-1], True)
        self.set_visibility([i[0] for i in self.grid], True)
        self.set_visibility([i[-1] for i in self.grid], True)

        # Now, see if we can see THROUGH the trees:
        # From the left:
        for yidx, row in enumerate(self.grid):
            for xidx, tree in enumerate(row):
                # Create a list of numbers above, below, to the left, and to the right of these indexes
                # Test if it can get past all of them to the outside.
                line_of_sight = [
                    self.get_tree_line_heights(xidx, yidx - 1, xidx - 1, -1),
                    self.get_tree_line_heights(
                        xidx, yidx + 1, xidx + 1, len(self.grid)
                    ),
                    self.get_tree_line_heights(0, yidx, xidx, yidx + 1),
                    self.get_tree_line_heights(xidx + 1, yidx, len(row), yidx + 1),
                ]
                for line in line_of_sight:
                    if all(tree.height > x for x in line):
                        tree.visible = True

    def get_tree_line_heights(self, x1, y1, x2, y2):
        """
        Function that uses coordinates to create a line of trees
        or a slice of the forest in any given direction
        and return the result as a list of tree heights
        """
        if x1 < 0 or y1 < 0:
            return []
        coordinates = []

        if x2 < x1:
            xstep = -1
        else:
            xstep = 1

        if y2 < y1:
            ystep = -1
        else:
            ystep = 1

        for x in range(x1, x2, xstep):
            for y in range(y1, y2, ystep):
                coordinates.append((x, y))
        heights = []

        for x, y in coordinates:
            heights.append(self.grid[y][x].height)
        return heights

    def show_forest(self):
        """
        Function to show the forest in a grid with
        all the recorded heights. Useful in debugging.
        """
        for row in self.grid:
            print("".join([str(tree.height) for tree in row]))
        return

    def show_visibility(self):
        """
        Function to show the current visibility state of
        all trees in the forest. Useful when debugging.
        """
        for row in self.grid:
            print("".join([tree.get_visibility() for tree in row]))
        return

    def show_view(self):
        """
        Function used in part 2 to debug the line of sight
        issue. This outputs the calculated line of sight
        [Up,Down,Left,Right] for each tree in the forest.
        """
        for row in self.grid:
            print(
                "\t".join(
                    [
                        "".join([str(item) for item in tree.view_distance])
                        for tree in row
                    ]
                )
            )
        return


class Point:
    """
    Stores information about a given point (e.g. tree)
    in the forest
    """

    def __init__(self, height):
        self.height = height
        self.visible = False
        self.view_distance = []
        self.view_score = 0

    def get_visibility(self):
        """
        Debug function to help display the visibility of
        this tree in an easy-to-read way
        """
        if self.visible:
            return "V"
        else:
            return "-"


def run(data):
    # Store the data in a structure
    this_forest = Forest()
    for row in data:
        grid_row = []
        for tree in row.strip():
            if tree.isnumeric():
                this_tree = Point(int(tree.strip()))
                grid_row.append(this_tree)
        this_forest.grid.append(grid_row)

    # Find the solution
    this_forest.find_visible_trees()
    return this_forest.count_visible_trees()


def run_p2(data):
    # Store the data in a structure
    this_forest = Forest()
    for row in data:
        grid_row = []
        for tree in row.strip():
            if tree.isnumeric():
                this_tree = Point(int(tree.strip()))
                grid_row.append(this_tree)
        this_forest.grid.append(grid_row)

    # Find the solution
    score = this_forest.find_view_distance()
    return score
