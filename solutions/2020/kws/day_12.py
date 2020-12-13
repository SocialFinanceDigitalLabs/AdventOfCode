#!/usr/bin/env python
import argparse
import math
from collections import namedtuple
from time import sleep

Coordinates = namedtuple('Coordinates', 'x y')


class Ship:

    def __init__(self, x, y, heading: int):
        self.x = x
        self.y = y
        self.heading = heading

    def __repr__(self):
        x = "E" if self.x >= 0 else "W"
        y = "S" if self.y >= 0 else "N"
        return f"{abs(self.x)}{x} {abs(self.y)}{y} {self.heading}°"


class Navigator:

    @staticmethod
    def move(ship, instruction):
        method = instruction[0]
        value = int(instruction[1:])
        function = getattr(Navigator, method)
        function(ship, value)

    @staticmethod
    def N(ship: Ship, speed):
        ship.y = ship.y - speed

    @staticmethod
    def S(ship: Ship, speed):
        ship.y = ship.y + speed

    @staticmethod
    def E(ship: Ship, speed):
        ship.x = ship.x + speed

    @staticmethod
    def W(ship: Ship, speed):
        ship.x = ship.x - speed

    @staticmethod
    def L(ship: Ship, degrees):
        ship.heading = (ship.heading + degrees) % 360

    @staticmethod
    def R(ship: Ship, degrees):
        ship.heading = (ship.heading - degrees) % 360

    @staticmethod
    def F(ship: Ship, speed):
        offset_x = math.sin(math.radians(ship.heading))
        offset_y = math.cos(math.radians(ship.heading))
        ship.x = round(ship.x + speed * offset_x)
        ship.y = round(ship.y + speed * offset_y)


class WayPointNavigator:

    @staticmethod
    def move(ship, waypoint, instruction):
        method = instruction[0]
        value = int(instruction[1:])
        function = getattr(WayPointNavigator, method)
        function(ship, waypoint, value)

    @staticmethod
    def rotate(px, py, angle):
        dx = math.cos(angle) * px - math.sin(angle) * py
        dy = math.sin(angle) * px + math.cos(angle) * py
        return round(dx), round(dy)

    @staticmethod
    def N(ship: Ship, waypoint: Ship, value):
        waypoint.y = waypoint.y - value

    @staticmethod
    def S(ship: Ship, waypoint: Ship, value):
        waypoint.y = waypoint.y + value

    @staticmethod
    def E(ship: Ship, waypoint: Ship, value):
        waypoint.x = waypoint.x + value

    @staticmethod
    def W(ship: Ship, waypoint: Ship, value):
        waypoint.x = waypoint.x - value

    @staticmethod
    def L(ship: Ship, waypoint: Ship, degrees):
        waypoint.x, waypoint.y = WayPointNavigator.rotate(waypoint.x, waypoint.y, math.radians(-degrees))

    @staticmethod
    def R(ship: Ship, waypoint: Ship, degrees):
        waypoint.x, waypoint.y = WayPointNavigator.rotate(waypoint.x, waypoint.y, math.radians(degrees))

    @staticmethod
    def F(ship: Ship, waypoint: Ship, speed):
        ship.x = ship.x + waypoint.x * speed
        ship.y = ship.y + waypoint.y * speed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 12 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--debug', '-d', action='store_true', help='Print debug output of maps')
    parser.add_argument('--turtle', action='store_true', help='Add a turtle')

    args = parser.parse_args()

    with args.file as FILE:
        input_lines = FILE.readlines()
    input_lines = [i.strip() for i in input_lines if len(i.strip()) > 0]

    ShipShape = namedtuple("ShipShape", "instruction x y heading text")
    ship = Ship(0, 0, 90)

    states = []
    for i in input_lines:
        Navigator.move(ship, i)
        states.append(ShipShape(i, ship.x, ship.y, ship.heading, repr(ship)))

    max_x = max([0] + [ship.x for ship in states])
    min_x = min([0] + [ship.x for ship in states])
    max_y = max([0] + [ship.y for ship in states])
    min_y = min([0] + [ship.y for ship in states])

    x_scale = max_x - min_x
    y_scale = max_y - min_y

    if args.turtle:
        import turtle
        screen = turtle.Screen()
        turtle.tracer(3)
        screen.setworldcoordinates(min_x - x_scale/10, min_y - y_scale/10, max_x + x_scale/10, max_y + y_scale/10)
        turtle_ship = turtle.Turtle()

    for ship in states:
        if args.turtle:
            turtle_ship.setheading(90-ship.heading)
            turtle_ship.goto(ship.x, ship.y)
            turtle.update()
        if args.debug:
            print(ship.instruction, ship.text)

    print(f"At the end of part 1 the ship is at {ship} with a manhattan distance of {abs(ship.x) + abs(ship.y)}")

    if args.turtle:
        sleep(2)

    states = []
    waypoints = []
    ship = Ship(0, 0, 0)
    waypoint = Ship(10, -1, 0)

    for i in input_lines:
        WayPointNavigator.move(ship, waypoint, i)
        states.append(ShipShape(i, ship.x, ship.y, ship.heading, repr(ship)))
        waypoints.append(ShipShape(i, waypoint.x, waypoint.y, waypoint.heading, repr(waypoint)))

    max_x = max([0] + [ship.x for ship in states] + [ship.x for ship in waypoints])
    min_x = min([0] + [ship.x for ship in states] + [ship.x for ship in waypoints])
    max_y = max([0] + [ship.y for ship in states] + [ship.y for ship in waypoints])
    min_y = min([0] + [ship.y for ship in states] + [ship.y for ship in waypoints])

    x_scale = max_x - min_x
    y_scale = max_y - min_y

    if args.turtle:
        screen.reset()
        screen.setworldcoordinates(min_x - x_scale/10, min_y - y_scale/10, max_x + x_scale/10, max_y + y_scale/10)

        turtle_ship.shape("circle")
        turtle_ship.turtlesize(.1, .1)

        turtle_waypoint = turtle.Turtle()
        turtle_waypoint.shape("square")
        turtle_waypoint.turtlesize(.1, .1)
        turtle_waypoint.color("red")

    for ix, ship in enumerate(states):
        waypoint = waypoints[ix]
        if args.turtle:
            turtle_ship.setheading(90 - ship.heading)
            turtle_waypoint.goto(ship.x + waypoint.x, ship.y + waypoint.y)
            turtle_ship.goto(ship.x, ship.y)
            turtle.update()

        if args.debug:
            print(ship.instruction, ship.text, waypoint.text)

    print(f"At the end of part 2 the ship is at {ship} with a manhattan distance of {abs(ship.x) + abs(ship.y)}")

    if args.turtle:
        input("Press any key to continue")
