from game import Game
from grid import Grid
from agents import MiniMaxAgent, ExpectimaxAgent
from evaluation import (
    random_heuristic,
    corner_heuristic,
    score_heuristic,
    empty_heuristic,
    unique_heuristic,
    monotonicity_heuristic,
    smoothness_heuristic,
)

DEPTH = 3
BATCH = 500


def playSingleGame(agent=MiniMaxAgent, eval=random_heuristic, depth=3):
    a = agent(eval, depth)
    game = Game(Grid(4)).setup()
    while not game.isOver():
        game = game.move(a.getAction(game)).addRandomTile()
    game.grid.print_grid()
    print("Score:", game.score)


def play(agent=MiniMaxAgent, eval=random_heuristic, depth=3, batch=100):
    a = agent(eval, depth)
    for i in range(batch):
        game = Game(Grid(4)).setup()
        while not game.isOver():
            game = game.move(a.getAction(game)).addRandomTile()

        with open("result.csv", "a") as f:
            f.write(f"{a.__class__.__name__},{eval.__name__},{depth},{game.score}\n")


def write_header():
    with open("result.csv", "w") as f:
        f.write("agent,eval,depth,score\n")


def generate():
    write_header()

    agents = [MiniMaxAgent, ExpectimaxAgent]
    evals = [
        random_heuristic,
        corner_heuristic,
        score_heuristic,
        empty_heuristic,
        unique_heuristic,
        monotonicity_heuristic,
        smoothness_heuristic,
    ]

    for agent in agents:
        for eval in evals:
            for depth in range(1, DEPTH + 1):
                play(agent, eval, depth, BATCH)


# generate()
playSingleGame(agent=ExpectimaxAgent, eval=score_heuristic, depth=3)
