from game import Game
from evaluation import score_heuristic


class ExpectimaxAgent:
    def __init__(self, eval=score_heuristic, depth=3) -> None:
        self.eval = eval
        self.depth = depth

    def getAction(self, gameState: Game):
        def maxAgent(game: Game, depth: int) -> float:
            if depth == 0 or game.isOver():
                return self.eval(game)

            v = -float("inf")
            for _, state in game.getLegalActions():
                v = max(v, expAgent(state, depth - 1))
            return v

        def expAgent(game: Game, depth: int) -> float:
            if depth == 0 or game.isOver():
                return self.eval(game)

            v = 0
            positions = game.grid.get_empty_positions()
            for position in positions:
                expectimax = 0
                for value in [(1, 0.9), (2, 0.1)]:
                    expectimax += value[1] * maxAgent(
                        game.addTile(*position, value[0]), depth - 1
                    )
                v += expectimax / len(positions)

            return v

        legalActions = gameState.getLegalActions()

        best_action = None
        best_score = -float("inf")
        for action, state in legalActions:
            score = expAgent(state, self.depth)
            if score > best_score:
                best_action = action
                best_score = score

        return best_action
