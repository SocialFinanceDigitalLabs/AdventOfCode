from util import FileParser
import os
from dataclasses import dataclass
import re
import numpy as np
import matplotlib.pyplot as plt
import math

dir_path = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Race:
    duration: int
    distance: int

    def find_wins_slow(self) -> int:
        wins = 0
        for time in range(1, self.duration):
            distance_traveled = (self.duration - time) * time
            if distance_traveled > self.distance:
                wins += 1
        return wins

    def plot(self):
        """
        the problem can be represented with a quadratic functon
        distance_traveled = (self.duration - time)*time
        <=> distance_traveled = self.duration*time - time**2
        """
        time = np.arange(1, self.duration, 1)
        distance_traveled = self.duration * time - time**2
        plt.plot(time, distance_traveled)

        # the distance we need to beat
        plt.axhline(y=self.distance, color="r", linestyle="dashed")

        plt.title("distance traveled")
        plt.xlabel("hold button time")
        plt.ylabel("distance")
        plt.show()

    def find_wins_quickly(self) -> int:
        """
        to apply the quadratic formula, convert the above (self.plot()) equation to:
        -time**2 + duration*time > self.distance

        if you assign time to x:
        x = time

        you have a more classic equation:
        -x**2 + duration*x - self.distance > 0

        where:
        """
        a = -1
        b = self.duration
        c = -self.distance
        # to solve the eqution
        # (-b ± (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        d = b**2 - 4 * a * c
        start = (-b + math.sqrt(d)) / (2 * a)
        end = (-b - math.sqrt(d)) / (2 * a)

        # find integers between range
        start = math.ceil(start) if start % 1 != 0 else int(start) + 1
        end = math.floor(end) if end % 1 != 0 else int(end) - 1
        return end - start + 1


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    durations = [int(d) for d in data[0].split(" ") if d.isdigit()]
    distances = [int(d) for d in data[1].split(" ") if d.isdigit()]
    races = [
        Race(duration, distance) for duration, distance in zip(durations, distances)
    ]
    result = 1
    for race in races:
        wins = race.find_wins_quickly()
        result *= wins
        # race.plot()

    return result


def part_2(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    duration = int(re.sub("[^0-9]", "", data[0]))
    distance = int(re.sub("[^0-9]", "", data[1]))
    race = Race(duration, distance)
    # race.plot()
    return race.find_wins_quickly()
