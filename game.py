from grid import Grid
import random
from typing import TypeVar
from collections import defaultdict


class Direction:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


T = TypeVar("T", bound="Game")


class Game:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.score = 0
        self.records = defaultdict(int)

    def setup(self: T) -> T:
        return self.fromState().addRandomTile().addRandomTile()

    def fromState(self: T) -> T:
        s = Game(self.grid.from_grid())
        s.score = self.score
        s.records = self.records.copy()
        return s

    def addRandomTile(self: T) -> T:
        # Adds a random tile to the grid
        available_positions = self.grid.get_empty_positions()

        if len(available_positions) == 0:
            return self

        # Choose a random position
        position = random.choice(available_positions)

        # Choose a random value
        value = 1 if random.random() < 0.9 else 2

        return self.addTile(*position, value)

    def addTile(self: T, x: int, y: int, value: int) -> T:
        s = self.fromState()
        s.grid.add_tile(x, y, value)
        return s

    def getLegalActions(self: T) -> list[(Direction, T)]:
        res = []

        if self.isOver():
            return res

        for direction in [
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT,
            Direction.UP,
        ]:
            next_state = self.move(direction)

            if next_state != self:
                res.append((direction, next_state))
        return res

    def move(self: T, direction: Direction) -> T:
        s = self.fromState()
        n = s.grid.size

        for x in range(n):
            stack = []
            for y in range(n):
                _x, _y = (
                    (y, x)
                    if direction == Direction.UP or direction == Direction.DOWN
                    else (x, y)
                )
                i = -_x - 1 if direction == Direction.DOWN else _x
                j = (
                    -_y - 1
                    if direction == Direction.DOWN or direction == Direction.RIGHT
                    else _y
                )

                tile = s.grid.get_tile(i, j)

                if len(stack) == 0:
                    if tile is not None:
                        stack.append([tile, False])
                else:
                    if stack[-1][0] == tile and not stack[-1][1]:
                        stack[-1][0] += 1
                        stack[-1][1] = True
                        s.score += 2 ** stack[-1][0]
                        if stack[-1][0] > 8:
                            s.records[2 ** stack[-1][0]] += 1
                    else:
                        if tile is not None:
                            stack.append([tile, False])

            for k in range(n):
                _x, _y = (
                    (k, x)
                    if direction == Direction.UP or direction == Direction.DOWN
                    else (x, k)
                )
                i = -_x - 1 if direction == Direction.DOWN else _x
                j = (
                    -_y - 1
                    if direction == Direction.DOWN or direction == Direction.RIGHT
                    else _y
                )

                s.grid.set_tile(i, j, stack[k][0] if k < len(stack) else None)

        return s

    def tileMatchesAvailable(self) -> bool:
        n = self.grid.size
        for i in range(n):
            for j in range(n):
                tile = self.grid.get_tile(i, j)

                if tile:
                    if self.grid.within_bounds(i, j + 1) and tile == self.grid.get_tile(
                        i, j + 1
                    ):
                        return True
                    if self.grid.within_bounds(i, j - 1) and tile == self.grid.get_tile(
                        i, j - 1
                    ):
                        return True
                    if self.grid.within_bounds(i + 1, j) and tile == self.grid.get_tile(
                        i + 1, j
                    ):
                        return True
                    if self.grid.within_bounds(i - 1, j) and tile == self.grid.get_tile(
                        i - 1, j
                    ):
                        return True

        return False

    def isOver(self) -> bool:
        return (
            len(self.grid.get_empty_positions()) == 0
            and not self.tileMatchesAvailable()
        )

    def __eq__(self, other):
        if not isinstance(other, Game):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.grid == other.grid
