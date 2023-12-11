from game import Game
from grid import Grid
from agents import ExpectimaxAgent
from evaluation import (
    random_heuristic,
    corner_heuristic,
    corner2_heuristic,
    score_heuristic,
    empty_heuristic,
    unique_heuristic,
    monotonicity_heuristic,
    monotonicity2_heuristic,
    smoothness_heuristic,
    max_tile_heuristic,
    weighted_heuristic,
)
import time

DEPTH = 4
BATCH = 50
FILE = "pre_result.csv"


def playSingleGame(eval=score_heuristic, depth=3):
    a = ExpectimaxAgent(eval, depth)
    game = Game(Grid(4)).setup()
    while not game.isOver():
        game = game.move(a.getAction(game)).addRandomTile()
        game.grid.print_grid()
    game.grid.print_grid()
    print("Score:", game.score, "Records:", game.records)


def play(eval=random_heuristic, depth=3, batch=100):
    a = ExpectimaxAgent(eval, depth)
    total_time = 0
    steps = 0
    for i in range(batch):
        game = Game(Grid(4)).setup()
        while not game.isOver():
            time_start = time.time()
            game = game.move(a.getAction(game)).addRandomTile()
            steps += 1
            end_time = time.time()
            total_time += end_time - time_start

        with open(FILE, "a") as f:
            f.write(
                f"{eval.__name__},{game.score},{game.records[512]},{game.records[1024]},{game.records[2048]},{total_time/steps}\n"
            )


def write_header():
    with open(FILE, "w") as f:
        f.write("eval,score,512,1024,2048,ave_time_per_step\n")


def generate():
    write_header()

    evals = [
        random_heuristic,
        score_heuristic,
        max_tile_heuristic,
        corner_heuristic,
        corner2_heuristic,
        unique_heuristic,
        empty_heuristic,
        smoothness_heuristic,
        monotonicity_heuristic,
        monotonicity2_heuristic,
        weighted_heuristic,
    ]

    for eval in evals:
        play(eval, DEPTH, BATCH)


# generate()
playSingleGame(eval=smoothness_heuristic, depth=5)
