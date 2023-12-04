from game import Game
from grid import Grid
import random


def random_heuristic(game: Game) -> float:
    return random.random()


def corner_heuristic(game: Game) -> float:
    size = game.grid.size
    weights = [[x + y for y in range(size)] for x in range(size)]

    h = 0
    for i in range(size):
        for j in range(size):
            tile = game.grid.get_tile(i, j)
            if tile:
                h += tile * (4 ** weights[i][j])
    return h


def score_heuristic(game: Game) -> float:
    return game.score


def empty_heuristic(game: Game) -> float:
    return len(game.grid.get_empty_positions()) ** 3


def unique_heuristic(game: Game) -> float:
    dic = {}
    for i in range(game.grid.size):
        for j in range(game.grid.size):
            tile = game.grid.get_tile(i, j)
            if tile:
                if tile in dic:
                    dic[tile] += 1
                else:
                    dic[tile] = 1

    return sum([dic[tile] ** 3 for tile in dic])


def smoothness_heuristic(game: Game) -> float:
    smoothness = 0
    for i in range(game.grid.size):
        for j in range(game.grid.size):
            tile = game.grid.get_tile(i, j)
            if tile:
                for k in range(1, 3):
                    if i + k < game.grid.size:
                        tile2 = game.grid.get_tile(i + k, j)
                        if tile2:
                            smoothness -= abs(tile - tile2)
                    if j + k < game.grid.size:
                        tile2 = game.grid.get_tile(i, j + k)
                        if tile2:
                            smoothness -= abs(tile - tile2)
    return smoothness


# https://github.com/ovolve/2048-AI/blob/master/js/ai.js
def monotonicity_heuristic(game: Game) -> float:
    best = -1
    for i in range(4):
        current = 0
        for row in range(3):
            for col in range(2):
                tile1 = game.grid.get_tile(row, col)
                tile2 = game.grid.get_tile(row, col + 1)
                if tile1 is not None and tile2 is not None and tile1 >= tile2:
                    current += tile1 - tile2
        for col in range(3):
            for row in range(2):
                tile1 = game.grid.get_tile(row, col)
                tile2 = game.grid.get_tile(row + 1, col)
                if tile1 is not None and tile2 is not None and tile1 >= tile2:
                    current += tile1 - tile2
        if current > best:
            best = current
        game.grid = rotate_grid(game.grid)  # Rotate the board 90 degrees clockwise
    return best


def rotate_grid(grid: Grid):
    # rotate the grid 90 degrees clockwise
    new_grid = Grid(grid.size)
    for i in range(grid.size):
        for j in range(grid.size):
            new_grid.set_tile(j, grid.size - 1 - i, grid.get_tile(i, j))
    return new_grid
