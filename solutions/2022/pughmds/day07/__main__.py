from anytree import Node, NodeMixin, LevelOrderGroupIter, PreOrderIter, RenderTree

"""
Second test made because I was passing tests, but live run was failing
"""
EXPECTED_TEST_ANSWER_PART1 = [95437, 95509]
EXPECTED_TEST_ANSWER_PART2 = [24933642, 24933642]

TOTAL_SPACE = 70000000
DIR_SIZE_LIMIT = 100000
SPACE_REQUIRED = 30000000


class File:
    """For storing file data"""

    def __init__(self, name, size):
        self.size = size
        self.name = name


class DirectoryNode(NodeMixin):
    """
    Decided to play around with AnyTree Library for this
    to learn how it works and handles tree structures.
    It also can output pretty pictures of the trees
    you make to help visualise it. This helped me
    be able to debug problems more easily
    https://anytree.readthedocs.io/en/latest/intro.html#overview
    """

    def __init__(self, name, parent=None):
        self.files = []
        self.name = name
        self.parent = parent
        self.sub_folders = []

    def get_size(self):
        """
        Adds up the sizes of all the files in this directory
        along with any subdirectories and returns the result
        """
        size = 0
        for file in self.files:
            size += file.size
        for folder in self.sub_folders:
            size += folder.get_size()
        return size


def print_tree(root):
    """
    A simple function which outputs an ASCII tree picture
    """
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def traverse(folder, limit=False):
    """
    Loops over all the objects and adds
    sizes only if they match given rules
    """
    sizes = []
    folder_size = folder.get_size()
    if limit:
        # For part 2, we want sizes LARGER than a given value
        if folder_size >= limit:
            sizes.append(folder_size)
    elif folder_size <= DIR_SIZE_LIMIT:
        # For part 1, we want to keep sizes BELOW a given value
        sizes.append(folder_size)
    for sub_folder in folder.sub_folders:
        # Recursion in Python is often not a good idea, but it works here
        sizes += traverse(sub_folder, limit)
    return sizes


def process_directory_change(entry, current_folder, root):
    """
    This handles a directory change and all the possible options
    """
    if ".." in entry:
        if current_folder.parent is not None:
            # Just in case there are intentional errors where the
            # User types "cd .." when they're already at root level
            current_folder = current_folder.parent
    elif "/" in entry:
        # I never actually saw this anywhere in my input...
        current_folder = root
    else:
        new_name = entry[4:].strip()
        # See if the subdirectory is already part of the tree structure
        sub_node = [
            node for node in current_folder.sub_folders if node.name == new_name
        ]
        if len(sub_node) == 0:
            # This is a new node
            new_directory = DirectoryNode(new_name, parent=current_folder)
            current_folder.sub_folders.append(new_directory)
            current_folder = new_directory
        else:
            # This node already exists
            current_folder = sub_node[0]
    return current_folder


def process_file(entry, current_folder):
    """
    This handles what to do when we find a file in a
    directory listing
    """
    size, file = entry.split(" ")[0:2]
    if size == "dir":
        # This listing is a subdirectory...nothing to do
        return current_folder
    else:
        # This is a file
        file_exists = False
        for old_file in current_folder.files:
            # Does the file already exist in the listing as a duplicate?
            if old_file.name == file and old_file.size == int(size):
                file_exists = True
        if not file_exists:
            # File is okay to add to the tree
            current_folder.files.append(File(file, int(size)))
    return current_folder


def process_entry(entry, current_folder, root):
    """
    Controlling function to handle all commands,
    and branch to CD or LS as needed
    """
    if entry.startswith("$"):
        if entry[2:].startswith("cd"):
            current_folder = process_directory_change(entry, current_folder, root)
    else:
        current_folder = process_file(entry, current_folder)
    return current_folder


def run(data):
    root = DirectoryNode("/", parent=None)
    current_folder = root
    for entry in data:
        current_folder = process_entry(entry, current_folder, root)

    # print_tree(root)

    sizes = traverse(root)
    return sum(sizes)


def run_p2(data):
    root = DirectoryNode("/", parent=None)
    current_folder = root
    for entry in data:
        current_folder = process_entry(entry, current_folder, root)

    current_used_space = root.get_size()
    free_space = TOTAL_SPACE - current_used_space
    needed_space = SPACE_REQUIRED - free_space

    sizes = traverse(root, limit=needed_space)
    sizes.sort()
    return sizes[0]
