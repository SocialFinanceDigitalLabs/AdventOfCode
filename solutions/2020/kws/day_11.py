#!/usr/bin/env python
import argparse
from collections import namedtuple
from enum import Enum
from typing import List, Iterator, Generic, TypeVar

T = TypeVar('T')
Coordinates = namedtuple('Coordinates', 'x y')
MAX_VALUE = 10000


class SeatState(Enum):
    EMPTY = "L"
    FLOOR = "."
    OCCUPIED = "#"


class Seat:
    """
    Represents a seat with a changeable state and hashable coordinates
    >>> Seat(Coordinates(0, 0), SeatState.FLOOR)
    (0, 0, .)

    """

    def __init__(self, coords: Coordinates, state: SeatState):
        self.coords = coords
        self.state = state

    def __repr__(self):
        return f"({self.coords.x}, {self.coords.y}, {self.state.value})"

    @property
    def x(self):
        return self.coords.x

    @property
    def y(self):
        return self.coords.y


class WaitingArea(Generic[T]):

    def __init__(self):
        self.seat_map = dict()

    def __str__(self):
        def print_row(y):
            row = []
            for x in range(0, MAX_VALUE):
                seat = self.seat_map.get(Coordinates(x, y))
                if seat is None:
                    return "".join(row)
                row.append(seat.state.value)

        value = []
        for y in range(0, MAX_VALUE):
            row = print_row(y)
            if len(row) == 0:
                return "\n".join(value)
            value.append(row)

    def add_seat(self, coords: Coordinates, initial_state: SeatState) -> Seat:
        seat = Seat(coords, initial_state)
        self.seat_map[coords] = seat
        return seat

    def get_surrounding_seats(self, coords: Coordinates) -> List[Seat]:
        surrounding = [
            Coordinates(coords.x + x, coords.y + y)
            for x in [-1, 0, 1]
            for y in [-1, 0, 1]
            if (x, y) != (0, 0)
        ]
        seats = [self.seat_map.get(c) for c in surrounding]
        seats = [s for s in seats if s is not None]
        return seats

    def get_first_seat_in_direction(self, coords: Coordinates, dir: Coordinates) -> Seat:
        for distance in range(1, MAX_VALUE):  # Note fixed size here to avoid infinite loops
            pos = Coordinates(coords.x + dir.x * distance, coords.y + dir.y * distance)
            seat = self.seat_map.get(pos)
            if seat is None:
                return Seat(pos, SeatState.FLOOR)
            if seat.state != SeatState.FLOOR:
                return seat
        raise OverflowError("Max iterations reached")

    def get_visible_seats(self, coords: Coordinates) -> List[Seat]:
        directions = [
            Coordinates(x, y)
            for x in [-1, 0, 1]
            for y in [-1, 0, 1]
            if (x, y) != (0, 0)
        ]
        seats = []
        for d in directions:
            seats.append(self.get_first_seat_in_direction(coords, d))

        return seats

    def get_seats_in_state(self, state: SeatState) -> List[Seat]:
        return self.__get_seats_in_state(self.seat_map.values(), state)

    @staticmethod
    def __get_seats_in_state(seats: Iterator[Seat], state: SeatState) -> List[Seat]:
        return [s for s in seats if s.state == state]

    def apply_rules(self, use_visible=False, max_seats=4) -> T:
        """
        Returns a new seat WaitingArea representing the new state
        :return:
        """
        waiting_area = WaitingArea()
        for s in self.seat_map.values():
            if use_visible:
                surrounding = self.get_visible_seats(s.coords)
            else:
                surrounding = self.get_surrounding_seats(s.coords)
            new_state = s.state
            if s.state == SeatState.EMPTY and len(self.__get_seats_in_state(surrounding, SeatState.OCCUPIED)) == 0:
                new_state = SeatState.OCCUPIED
            if s.state == SeatState.OCCUPIED and len(self.__get_seats_in_state(surrounding,
                                                                               SeatState.OCCUPIED)) >= max_seats:
                new_state = SeatState.EMPTY
            waiting_area.add_seat(s.coords, new_state)
        return waiting_area


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 11 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--debug', '-d', action='store_true', help='Print debug output of maps')
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    if args.test:
        import doctest

        doctest.testmod()
        print("Tests completed")
        exit(0)

    with args.file as FILE:
        input_lines = FILE.readlines()

    original_wa = WaitingArea()
    seats = [
        original_wa.add_seat(Coordinates(x, y), SeatState(char))
        for y, line in enumerate(input_lines)
        for x, char in enumerate(line.strip())
    ]

    wa = original_wa
    occupied_seats = -1
    while len(wa.get_seats_in_state(SeatState.OCCUPIED)) != occupied_seats:
        occupied_seats = len(wa.get_seats_in_state(SeatState.OCCUPIED))
        if args.debug:
            print(f"{occupied_seats} occupied seats")
            print(wa, end="\n\n")
        wa = wa.apply_rules()

    print(f"For part 1 there are {occupied_seats} occupied seats.")

    wa = original_wa
    occupied_seats = -1
    while len(wa.get_seats_in_state(SeatState.OCCUPIED)) != occupied_seats:
        occupied_seats = len(wa.get_seats_in_state(SeatState.OCCUPIED))
        if args.debug:
            print(f"{occupied_seats} occupied seats")
            print(wa, end="\n\n")
        wa = wa.apply_rules(use_visible=True, max_seats=5)

    print(f"For part 2 there are {occupied_seats} occupied seats.")
    if args.debug:
        print(wa)

