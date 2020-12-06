#! /usr/bin/env python
import sys
import re

with open(sys.argv[1], 'rt') as FILE:
    file_content = FILE.read().strip()

# Split groups by empty lines
groups = re.split(r"\n\n", file_content, flags=re.M)

# Count unique alpha characters in each group
unique = [{c for c in g if c.isalpha()} for g in groups]
counts = [len(p) for p in unique]
print(f"PART 1: There are {sum(counts)} questions where anyone answers yes")

# Within each group, create the intersection of answers for each person
group_answers = [[set(c) for c in re.split(r"\n", p)] for p in groups]
intersected_group_answers = [len(g[0].intersection(*g)) for g in group_answers]
print(f"PART 2: there are {sum(intersected_group_answers)} questions where everyone in the group answered yes")
