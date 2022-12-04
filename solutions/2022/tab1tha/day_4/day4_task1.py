import pandas as pd

with open("input_day4.txt", "r") as f:
    section_pairs = f.read()

# with open("test_input_day4.txt", "r") as f:
#     section_pairs = f.read()

section_pairs = section_pairs.split("\n")
section_pairs = [pair.split(",") for pair in section_pairs]
section_pairs = pd.DataFrame(section_pairs, columns=["one_elf", "other_elf"])

section_pairs[["one_start", "one_end"]] = section_pairs["one_elf"].str.split(
    "-", 1, expand=True
)
section_pairs[["other_start", "other_end"]] = section_pairs["other_elf"].str.split(
    "-", 1, expand=True
)
section_pairs.drop(["one_elf", "other_elf"], inplace=True, axis=1)

section_pairs = section_pairs.astype(int)

one_within_other = (section_pairs["one_start"] >= section_pairs["other_start"]) & (
    section_pairs["one_end"] <= section_pairs["other_end"]
)
other_within_one = (section_pairs["other_start"] >= section_pairs["one_start"]) & (
    section_pairs["other_end"] <= section_pairs["one_end"]
)
inside_another = section_pairs[one_within_other | other_within_one]

one_after_other = section_pairs["one_start"] > section_pairs["other_end"]
other_after_one = section_pairs["other_start"] > section_pairs["one_end"]
no_overlap = one_after_other | other_after_one
overlap = section_pairs[~(no_overlap)]

result1 = len(inside_another)
result2 = len(overlap)
