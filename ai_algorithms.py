import math
import copy

def heuristic(state):
    """
    Heuristic = favorable_pairs - (computer_score - human_score)
    
    favorable_pairs: count of '00' and '11' pairs in the current sequence
   
    """
    scores = state.get_scores()
    score_diff = scores[1] - scores[0]  # computer - human

    favorable_pairs = sum(
        1 for i in range(len(state.sequence) - 1)
        if (state.sequence[i] + state.sequence[i + 1]) in ("00", "11")
    )

    # pievieno -, jo dators ir maksimizetajs
    # Lower result = better for computer; higher = better for human.
    return -(favorable_pairs - score_diff)

class MinimaxAgent:
    def __init__(self, depth=4):
        self.depth = depth

    def choose_move(self, game_state):
        tree = build_game_tree(game_state, max_depth=self.depth)  # ģenerē koku
        best_move = self.minimax(tree)  # pārlūko koku
        return best_move

    def minimax(self, state, depth, is_maximizing):
        if depth == 0 or state.is_game_over():
            # Evaluation: Computer Score - Opponent Score
            scores = state.get_scores()
            # Computer is Player 2 (index 1) and Human is Player 1 (index 0)
            return heuristic(state)

        if is_maximizing:
            max_eval = -math.inf
            for idx, _ in state.get_available_pairs():
                child = copy.deepcopy(state)
                child.apply_move(idx)
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for idx, _ in state.get_available_pairs():
                child = copy.deepcopy(state)
                child.apply_move(idx)
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

class AlphaBetaAgent:
    def __init__(self, depth=5): # Can afford higher depth with Alpha-Beta
        self.depth = depth

    def choose_move(self, game_state):
        tree = build_game_tree(game_state, max_depth=self.depth)  # ģenerē koku
        best_move = self.minimax(tree)  # pārlūko koku
        return best_move

    def alphabeta(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or state.is_game_over():
            scores = state.get_scores()
            return heuristic(state)

        if is_maximizing:
            max_eval = -math.inf
            for idx, _ in state.get_available_pairs():
                child = copy.deepcopy(state)
                child.apply_move(idx)
                eval = self.alphabeta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for idx, _ in state.get_available_pairs():
                child = copy.deepcopy(state)
                child.apply_move(idx)
                eval = self.alphabeta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval
