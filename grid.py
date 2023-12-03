class Grid:
    def __init__(self, size: int):
        self.size = size
        self.grid = self.empty_grid()

    def empty_grid(self) -> list[list[int]]:
        return [[None for _ in range(self.size)] for _ in range(self.size)]

    def add_new(self, x: int, y: int, value: int):
        # Adds a tile to the grid at its position
        self.grid[x][y] = value

    def get_cell_value(self, x: int, y: int) -> int:
        # Returns the value of the cell at the given position
        return self.grid[x][y]
    
    def set_cell_value(self, x: int, y: int, value: int):
        # Sets the value of the cell at the given position
        self.grid[x][y] = value

    def get_empty_positions(self) -> list[tuple[int, int]]:
        # Returns a list of empty positions in the grid
        return [(x, y) for x in range(self.size) for y in range(self.size) if self.grid[x][y] is None]
        
    
    def print_grid(self):
      for row in self.grid:
          print("+----" * self.size + "+")
          print("|" + "|".join(f"{cell * 2 if cell is not None else '':^4}" for cell in row) + "|")
      print("+----" * self.size + "+")
      print("-----" * self.size + "+")