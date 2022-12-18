from collections import Counter

from aoc_2022_kws.day_18 import Cube


def test_faces():
    cube = Cube("1,2,3")
    faces = set(cube.faces)
    assert len(faces) == 6


def test_faces_combine():
    c1 = Cube("1,1,1")
    c2 = Cube("2,1,1")

    all_faces = list(c1.faces) + list(c2.faces)
    unique_faces = set(all_faces)

    assert len(all_faces) == 12
    assert len(unique_faces) == 11

    u = set.intersection(*[set(c.faces) for c in [c1, c2]])
    assert len(u) == 1

    assert len(set(all_faces) - u) == 10

    c3 = Cube("3,1,1")
    all_faces = list(c1.faces) + list(c2.faces) + list(c3.faces)
    assert len(all_faces) == 18
    assert len(set(all_faces)) == 16

    face_counts = Counter(all_faces)
    covered_faces = [f for f, c in face_counts.items() if c > 1]

    assert len(covered_faces) == 2
    assert len(set(all_faces) - set(covered_faces)) == 14
