from game import Game
from grid import Grid
import random
import math


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


def corner2_heuristic(game: Game) -> float:
    n = game.grid.size
    weights = [[0] * n for _ in range(n)]  # Initialize an n x n grid with zeros
    num = n * n - 1  # Start filling from the highest number

    for i in range(n):
        if i % 2 == 0:  # Even index rows are filled from right to left
            for j in range(n - 1, -1, -1):
                weights[i][j] = num
                num -= 1
        else:  # Odd index rows are filled from left to right
            for j in range(n):
                weights[i][j] = num
                num -= 1

    h = 0
    for i in range(n):
        for j in range(n):
            tile = game.grid.get_tile(i, j)
            if tile:
                h += tile * (4 ** weights[i][j])
    return h


def score_heuristic(game: Game) -> float:
    return game.score


def empty_heuristic(game: Game) -> float:
    return len(game.grid.get_empty_positions()) ** 3


def unique_heuristic(game: Game) -> float:
    counter = [0] * 17
    for i in range(game.grid.size):
        for j in range(game.grid.size):
            tile = game.grid.get_tile(i, j)
            if tile:
                counter[tile] += 1

    return sum(i**3 for i in counter)


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
    for i in range(2):
        current = 0
        for row in range(3):
            for col in range(2):
                tile1 = game.grid.get_tile(row, col)
                tile2 = game.grid.get_tile(row, col + 1)
                if tile1 is not None and tile2 is not None and tile1 >= tile2:
                    current += 1
        for col in range(3):
            for row in range(2):
                tile1 = game.grid.get_tile(row, col)
                tile2 = game.grid.get_tile(row + 1, col)
                if tile1 is not None and tile2 is not None and tile1 >= tile2:
                    current += 1
        if current > best:
            best = current
        game.grid = rotate_grid(game.grid)  # Rotate the board 90 degrees clockwise
    return best


def monotonicity2_heuristic(game: Game) -> float:
    totals = [0, 0, 0, 0]

    # up/down direction
    for x in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and not game.grid.get_tile(x, next):
                next += 1

            if next >= 4:
                next -= 1

            currentValue = (
                game.grid.get_tile(x, current) if game.grid.get_tile(x, current) else 0
            )
            nextValue = (
                game.grid.get_tile(x, current) if game.grid.get_tile(x, current) else 0
            )

            if currentValue > nextValue:
                totals[0] += nextValue - currentValue
            elif nextValue > currentValue:
                totals[1] += currentValue - nextValue
            current = next
            next += 1

    # left/right direction
    for y in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and not game.grid.get_tile(next, y):
                next += 1
            if next >= 4:
                next -= 1
            currentValue = (
                math.log(game.grid.get_tile(next, y)) / math.log(2)
                if game.grid.get_tile(next, y)
                else 0
            )
            nextValue = (
                math.log(game.grid.get_tile(next, y)) / math.log(2)
                if game.grid.get_tile(next, y)
                else 0
            )
            if currentValue > nextValue:
                totals[2] += nextValue - currentValue
            elif nextValue > currentValue:
                totals[3] += currentValue - nextValue
            current = next
            next += 1

    return max(totals[0], totals[1]) + max(totals[2], totals[3])


def max_tile_heuristic(game: Game) -> float:
    return max(
        [
            game.grid.get_tile(i, j) or 0
            for i in range(game.grid.size)
            for j in range(game.grid.size)
        ]
    )


def weighted_heuristic(game: Game) -> float:
    return (
        0.1 * smoothness_heuristic(game)
        + 2.7 * empty_heuristic(game)
        + 1 * max_tile_heuristic(game)
        + monotonicity2_heuristic(game)
    )


def rotate_grid(grid: Grid):
    # rotate the grid 90 degrees clockwise
    new_grid = Grid(grid.size)
    for i in range(grid.size):
        for j in range(grid.size):
            new_grid.set_tile(j, grid.size - 1 - i, grid.get_tile(i, j))
    return new_grid
