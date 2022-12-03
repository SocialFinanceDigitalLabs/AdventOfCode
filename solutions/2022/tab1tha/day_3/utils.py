def string_in_two(strng):
    """divide a string into two equal parts"""
    first_part = strng[: len(strng) // 2]
    second_part = strng[len(strng) // 2 :]
    return [first_part, second_part]


def common_element(first_part, second_part):
    # find element types that exist in both compartments.
    unique_firsts = set(list(first_part))
    unique_seconds = set(list(second_part))
    # set unpacking. Assumes that there is always only one common element.
    try:
        commoner, *_ = unique_firsts.intersection(unique_seconds)
    except:
        commoner = pd.NA
    # use list(set) and explode the dataframe to account for multiple commoners

    return commoner
