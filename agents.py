from game import Game
from evaluation import score_heuristic


class MiniMaxAgent:
    def __init__(self, eval=score_heuristic, depth=3) -> None:
        self.eavl = eval
        self.depth = depth

    def getAction(self, gameState: Game):
        def maxAgent(game: Game, depth: int, alpha: float, beta: float) -> float:
            if depth == 0 or game.isOver():
                return self.eavl(game)

            v = -float("inf")
            for position in game.grid.get_empty_positions():
                for value in [1, 2]:
                    v = max(
                        v,
                        minAgent(
                            game.addTile(*position, value), depth - 1, alpha, beta
                        ),
                    )
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def minAgent(game: Game, depth: int, alpha: float, beta: float) -> float:
            if depth == 0 or game.isOver():
                return self.eavl(game)

            v = float("inf")
            for _, state in game.getLegalActions():
                v = min(v, maxAgent(state, depth - 1, alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        legalActions = gameState.getLegalActions()

        best_action = None
        best_score = -float("inf")
        alpha = -float("inf")
        beta = float("inf")
        for action, state in legalActions:
            score = minAgent(state, self.depth, alpha, beta)
            if score > best_score:
                best_action = action
                best_score = score
            alpha = max(alpha, best_score)

        return best_action


class ExpectimaxAgent:
    def __init__(self, eval=score_heuristic, depth=3) -> None:
        self.eavl = eval
        self.depth = depth

    def getAction(self, gameState: Game):
        def maxAgent(game: Game, depth: int) -> float:
            if depth == 0 or game.isOver():
                return self.eavl(game)

            v = -float("inf")
            for position in game.grid.get_empty_positions():
                expectimax = 0
                for value in [(1, 0.9), (2, 0.1)]:
                    expectimax += value[1] * expAgent(
                        game.addTile(*position, value[0]), depth - 1
                    )
                v = max(v, expectimax)
            return v

        def expAgent(game: Game, depth: int) -> float:
            if depth == 0 or game.isOver():
                return self.eavl(game)

            v = 0
            for _, state in game.getLegalActions():
                v += maxAgent(state, depth - 1)
            return v / len(game.getLegalActions())

        legalActions = gameState.getLegalActions()

        best_action = None
        best_score = -float("inf")
        for action, state in legalActions:
            score = expAgent(state, self.depth)
            if score > best_score:
                best_action = action
                best_score = score

        return best_action
