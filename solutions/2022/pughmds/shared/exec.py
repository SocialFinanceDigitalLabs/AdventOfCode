def create_result(part_num, expected_answer=False):
    answer = {
        "Part": "Part {}".format(part_num),
    }
    if expected_answer:
        answer["Expected"] = expected_answer
    return answer
