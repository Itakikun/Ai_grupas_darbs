import math
import copy
import time
import random

from game_logic import GameState
from ai_algorithms import MinimaxAgent, AlphaBetaAgent, heuristic


# ─────────────────────────────────────────────────────────────────────────────
#  NODE-COUNTING WRAPPERS
#  Wrap each agent so we can track how many nodes were generated per search.
# ─────────────────────────────────────────────────────────────────────────────

class CountingMinimaxAgent(MinimaxAgent):
    """MinimaxAgent that counts every node it generates."""

    def __init__(self, depth=4):
        super().__init__(depth)
        self.nodes_generated = 0

    def choose_move(self, game_state):
        self.nodes_generated = 0
        best_score = -math.inf
        best_move = None

        for idx, _ in game_state.get_available_pairs():
            self.nodes_generated += 1                       # root children
            temp_state = copy.deepcopy(game_state)
            temp_state.apply_move(idx)
            score = self._minimax_counted(temp_state, self.depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = idx
        return best_move

    def _minimax_counted(self, state, depth, is_maximizing):
        if depth == 0 or state.is_game_over():
            return heuristic(state)

        if is_maximizing:
            max_eval = -math.inf
            for idx, _ in state.get_available_pairs():
                self.nodes_generated += 1
                child = copy.deepcopy(state)
                child.apply_move(idx)
                val = self._minimax_counted(child, depth - 1, False)
                max_eval = max(max_eval, val)
            return max_eval
        else:
            min_eval = math.inf
            for idx, _ in state.get_available_pairs():
                self.nodes_generated += 1
                child = copy.deepcopy(state)
                child.apply_move(idx)
                val = self._minimax_counted(child, depth - 1, True)
                min_eval = min(min_eval, val)
            return min_eval


class CountingAlphaBetaAgent(AlphaBetaAgent):
    """AlphaBetaAgent that counts every node it generates."""

    def __init__(self, depth=5):
        super().__init__(depth)
        self.nodes_generated = 0

    def choose_move(self, game_state):
        self.nodes_generated = 0
        best_score = -math.inf
        best_move = None

        for idx, _ in game_state.get_available_pairs():
            self.nodes_generated += 1                       # root children
            temp_state = copy.deepcopy(game_state)
            temp_state.apply_move(idx)
            score = self._alphabeta_counted(
                temp_state, self.depth - 1, -math.inf, math.inf, False
            )
            if score > best_score:
                best_score = score
                best_move = idx
        return best_move

    def _alphabeta_counted(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or state.is_game_over():
            return heuristic(state)

        if is_maximizing:
            max_eval = -math.inf
            for idx, _ in state.get_available_pairs():
                self.nodes_generated += 1
                child = copy.deepcopy(state)
                child.apply_move(idx)
                val = self._alphabeta_counted(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break                                   # prune
            return max_eval
        else:
            min_eval = math.inf
            for idx, _ in state.get_available_pairs():
                self.nodes_generated += 1
                child = copy.deepcopy(state)
                child.apply_move(idx)
                val = self._alphabeta_counted(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break                                   # prune
            return min_eval


# ─────────────────────────────────────────────────────────────────────────────
#  EXPERIMENT RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def _clone_state_with_sequence(original: GameState, sequence: list) -> GameState:
    """
    Return a fresh GameState that has the given sequence but is otherwise
    in the same starting configuration as `original`.
    Used so both agents always start from exactly the same board.
    """
    clone = copy.deepcopy(original)
    clone.sequence = list(sequence)      # explicit copy
    clone.scores = [0, 0]
    clone.current_player = 0
    clone.move_history = []
    return clone


def run_experiment(
    sequence_length: int = 15,
    minimax_depth: int = 4,
    alphabeta_depth: int = 5,
    num_rounds: int = 5,
    seed: int | None = None,
) -> None:
    """
    Run `num_rounds` full games.  In every round both algorithms receive the
    **identical** starting sequence.  The function prints a detailed per-round
    report and a summary table at the end.

    Parameters
    ----------
    sequence_length : int
        Length of the binary string for every game (must respect MIN/MAX from config).
    minimax_depth   : int
        Search depth for the Minimax agent.
    alphabeta_depth : int
        Search depth for the Alpha-Beta agent.
    num_rounds      : int
        Number of independent games to run.
    seed            : int | None
        Fixed random seed for reproducibility.  Pass None for random behaviour.
    """

    if seed is not None:
        random.seed(seed)

    mm_agent = CountingMinimaxAgent(depth=minimax_depth)
    ab_agent = CountingAlphaBetaAgent(depth=alphabeta_depth)

    # Accumulators for the summary table
    totals = {
        "minimax":   {"time": 0.0, "nodes": 0, "wins": 0},
        "alphabeta": {"time": 0.0, "nodes": 0, "wins": 0},
    }

    sep = "─" * 70

    print()
    print("=" * 70)
    print("  EKSPERIMENTS: Minimax vs Alpha-Beta salīdzinājums")
    print(f"  Virknes garums : {sequence_length}")
    print(f"  Minimax dziļums: {minimax_depth}  |  Alpha-Beta dziļums: {alphabeta_depth}")
    print(f"  Spēļu skaits   : {num_rounds}")
    print("=" * 70)

    for round_num in range(1, num_rounds + 1):
        # ── Generate ONE sequence that both agents will use ──────────────────
        template_state = GameState(sequence_length)
        shared_sequence = template_state.sequence[:]   # list of '0'/'1' strings

        print(f"\n{sep}")
        print(f"  Spēle {round_num}/{num_rounds}")
        print(f"  Sākuma virkne: {' '.join(shared_sequence)}")
        print(sep)

        round_data = {}

        for algo_name, agent in [("minimax", mm_agent), ("alphabeta", ab_agent)]:
            state = _clone_state_with_sequence(template_state, shared_sequence)

            total_time  = 0.0
            total_nodes = 0
            move_count  = 0

            # ── Play the full game ───────────────────────────────────────────
            while not state.is_game_over():
                agent.nodes_generated = 0

                t0 = time.perf_counter()
                move_idx = agent.choose_move(state)
                t1 = time.perf_counter()

                elapsed     = t1 - t0
                total_time  += elapsed
                total_nodes += agent.nodes_generated
                move_count  += 1

                if move_idx is None:
                    # No move available – shouldn't happen with is_game_over check,
                    # but guard against edge cases.
                    break

                state.apply_move(move_idx)

            scores = state.get_scores()
            winner = state.get_final_result_text()

            round_data[algo_name] = {
                "time":   total_time,
                "nodes":  total_nodes,
                "moves":  move_count,
                "scores": scores,
                "winner": winner,
            }

            totals[algo_name]["time"]  += total_time
            totals[algo_name]["nodes"] += total_nodes

            label = "Minimax    " if algo_name == "minimax" else "Alpha-Beta "
            print(
                f"  {label} | Laiks: {total_time:.4f}s "
                f"| Mezgli: {total_nodes:>8,} "
                f"| Gājieni: {move_count:>3} "
                f"| Rezultāts: {scores[0]:>3} – {scores[1]}"
            )
            print(f"            | {winner}")

        # ── Who won the round? ───────────────────────────────────────────────
        mm_scores = round_data["minimax"]["scores"]
        ab_scores = round_data["alphabeta"]["scores"]

        # Computer is player index 1 in both cases
        if mm_scores[1] > mm_scores[0]:
            totals["minimax"]["wins"] += 1
        if ab_scores[1] > ab_scores[0]:
            totals["alphabeta"]["wins"] += 1

        # Speed comparison for this round
        if round_data["minimax"]["time"] > 0:
            speedup = round_data["minimax"]["time"] / round_data["alphabeta"]["time"] \
                if round_data["alphabeta"]["time"] > 0 else float("inf")
            node_ratio = round_data["minimax"]["nodes"] / round_data["alphabeta"]["nodes"] \
                if round_data["alphabeta"]["nodes"] > 0 else float("inf")
            print(f"\n  → Alpha-Beta {speedup:.2f}x ātrāks šajā spēlē")
            print(f"  → Alpha-Beta apstrādāja {node_ratio:.2f}x mazāk mezglu")

    # ── Summary table ────────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print("  KOPSAVILKUMS")
    print(f"{'=' * 70}")
    print(f"  {'Algoritms':<14} {'Kop. laiks':>12} {'Kop. mezgli':>14} {'Uzvaras':>9}")
    print(f"  {'-'*14} {'-'*12} {'-'*14} {'-'*9}")

    for algo_name, label in [("minimax", "Minimax"), ("alphabeta", "Alpha-Beta")]:
        d = totals[algo_name]
        print(
            f"  {label:<14} {d['time']:>11.4f}s {d['nodes']:>14,} {d['wins']:>8}/{num_rounds}"
        )

    if totals["minimax"]["time"] > 0 and totals["alphabeta"]["time"] > 0:
        overall_speedup    = totals["minimax"]["time"]  / totals["alphabeta"]["time"]
        overall_node_ratio = totals["minimax"]["nodes"] / totals["alphabeta"]["nodes"] \
            if totals["alphabeta"]["nodes"] > 0 else float("inf")
        print(f"\n  Kopējais ātruma uzlabojums : Alpha-Beta ir {overall_speedup:.2f}x ātrāks")
        print(f"  Mezglu samazinājums        : Alpha-Beta apstrādāja {overall_node_ratio:.2f}x mazāk mezglu")

    print("=" * 70)
    print()


# ─────────────────────────────────────────────────────────────────────────────
#  QUICK ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
