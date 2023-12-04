from typing import TypeVar


T = TypeVar("T", bound="Grid")


class Grid:
    def __init__(self, size: int = 4):
        self.size = size
        self.grid = self.empty_grid()

    def from_grid(self: T):
        g = Grid(self.size)

        for x in range(self.size):
            for y in range(self.size):
                g.set_tile(x, y, self.grid[x][y])

        return g

    def empty_grid(self) -> list[list[int]]:
        return [[None for _ in range(self.size)] for _ in range(self.size)]

    def add_tile(self, x: int, y: int, value: int):
        # Adds a tile to the grid at its position
        if self.grid[x][y] is not None:
            raise Exception("Tile already exists at this position")
        self.grid[x][y] = value

    def get_tile(self, x: int, y: int) -> int:
        # Returns the value of the cell at the given position
        return self.grid[x][y]

    def set_tile(self, x: int, y: int, value: int):
        # Sets the value of the cell at the given position
        self.grid[x][y] = value

    def get_empty_positions(self) -> list[tuple[int, int]]:
        # Returns a list of empty positions in the grid
        return [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if self.grid[x][y] is None
        ]

    def within_bounds(self, x: int, y: int) -> bool:
        # Returns whether the given position is within the grid
        return 0 <= x < self.size and 0 <= y < self.size

    def __eq__(self, other):
        if not isinstance(other, Grid):
            # don't attempt to compare against unrelated types
            return NotImplemented

        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != other.grid[x][y]:
                    return False
        return True

    def print_grid(self):
        for row in self.grid:
            print("+----" * self.size + "+")
            print(
                "|"
                + "|".join(
                    f"{2 ** cell if cell is not None else '':^4}" for cell in row
                )
                + "|"
            )
        print("+----" * self.size + "+")
