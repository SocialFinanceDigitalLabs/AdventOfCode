from aocd import get_data
from collections import namedtuple

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

head_directions = get_data(day=9, year=2022, session=session).splitlines()

coordinates = namedtuple("coordinates", "x, y")


class Head:
    def __init__(self, coordinates=coordinates(0, 0)):
        self.coordinates = coordinates

    def move(self, direction):
        pass


