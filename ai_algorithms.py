import math
import copy
from game_tree import build_game_tree

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
        best_score = -math.inf
        best_move = None

        for child in tree.children:  # ← pārlūko koka bērnus
            score = self.minimax(child, self.depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = child.move_info["index"]  # ← ņem gājiena indeksu no move_info
        return best_move

    def minimax(self, node, depth, is_maximizing):  # ← node ir GameTreeNode, ne state
        if depth == 0 or node.state.is_game_over():
            return heuristic(node.state)  # ← heiristika no node.state

        if is_maximizing:
            max_eval = -math.inf
            for child in node.children:  # ← pārlūko bērnus, ne get_available_pairs
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in node.children:
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

class AlphaBetaAgent:
    def __init__(self, depth=5): # Can afford higher depth with Alpha-Beta
        self.depth = depth

    def choose_move(self, game_state):
        tree = build_game_tree(game_state, max_depth=self.depth)  # ģenerē koku
        best_score = -math.inf
        best_move = None

        for child in tree.children:  # ← pārlūko koka bērnus
            score = self.alphabeta(child, self.depth - 1, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_move = child.move_info["index"]  # ← ņem gājiena indeksu
        return best_move

    def alphabeta(self, node, depth, alpha, beta, is_maximizing):  # ← node, ne state
        if depth == 0 or node.state.is_game_over():
            return heuristic(node.state)  # ← heiristika no node.state

        if is_maximizing:
            max_eval = -math.inf
            for child in node.children:  # ← pārlūko bērnus
                eval = self.alphabeta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for child in node.children:  # ← pārlūko bērnus
                eval = self.alphabeta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval
