from functools import lru_cache

EXPECTED_TEST_ANSWER_PART1 = [1320]
EXPECTED_TEST_ANSWER_PART2 = [145]


@lru_cache(maxsize=None)
def hash(instruction):
    """
    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """
    current_value = 0
    for char in instruction:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value


def handle_instruction(instr, boxes):
    """
    A bit untidy, but sorts through the instructions and either stores,
    removes, or updates the boxes as needed.
    """
    label, focal = instr.split("=") if "=" in instr else instr.split("-")
    focal = int(focal) if focal else 0
    box = hash(label)

    if box not in boxes:
        if "=" in instr:
            boxes[box] = [{"label": label, "focal": focal}]
        return boxes

    if "=" in instr:
        # Update existing item or add new item
        for item in boxes[box]:
            if item["label"] == label:
                item["focal"] = focal
                return boxes
        else:
            boxes[box].append({"label": label, "focal": focal})
    else:
        # Remove item with matching label
        boxes[box] = [item for item in boxes[box] if item["label"] != label]

    return boxes


def score_focal_positions(boxes):
    """
    Go through each box and score it as follows:
    box number * Box Position * Focal Score
    """
    total = 0
    for key in boxes:
        if len(boxes[key]) == 0:
            continue
        else:
            for idx, item in enumerate(boxes[key]):
                total += (key + 1) * (idx + 1) * item["focal"]
    return total


def run(data):
    instructions = data[0].split(",")
    total = 0
    for instruction in instructions:
        total += hash(instruction)
    return total


def run_p2(data):
    instructions = data[0].split(",")
    boxes = {}
    for instruction in instructions:
        boxes = handle_instruction(instruction, boxes)

    return score_focal_positions(boxes)
