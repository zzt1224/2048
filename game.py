from grid import Grid
import random

class Game:
  def __init__(self, grid: Grid):
    self.grid = grid
    self.addRandomTile()
    self.addRandomTile()

  def addRandomTile(self):
    # Adds a random tile to the grid
    available_positions = self.grid.get_empty_positions()
    
    if len(available_positions) == 0:
      return False
    
    # Choose a random position
    position = random.choice(available_positions)

    # Choose a random value
    value = 1 if random.random() < 0.9 else 2

    self.grid.add_new(*position, value)
    return True
  
  def move(self, direction: str):
    n = self.grid.size
    moved = False

    for x in range(n):
      stack = []
      for y in range(n):
        _x, _y = (y, x) if direction == "UP" or direction == "DOWN" else (x, y)
        i = -_x - 1 if direction == "DOWN" else _x
        j = -_y - 1 if direction == "DOWN" or direction == "RIGHT" else _y

        if len(stack) == 0:
          cell = self.grid.get_cell_value(i, j)
          if cell is not None:
            stack.append(cell)
        else:
          if stack[-1] == self.grid.get_cell_value(i, j):
            stack[-1] += 1
          else:
            cell = self.grid.get_cell_value(i, j)
            if cell is not None:
              stack.append(cell)

      for k in range(n):
        _x, _y = (k, x) if direction == "UP" or direction == "DOWN" else (x, k)
        i = -_x - 1 if direction == "DOWN" else _x
        j = -_y - 1 if direction == "DOWN" or direction == "RIGHT" else _y
        
        new_value = stack[k] if k < len(stack) else None
        if self.grid.get_cell_value(i, j) != new_value:
          moved = True

        self.grid.set_cell_value(i, j, new_value)

    if moved:
      self.addRandomTile()

game = Game(Grid(5))
game.grid.print_grid()
game.move("LEFT")
game.move("LEFT")
game.move("LEFT")
game.grid.print_grid()



        





        
  
