import copy
from game_logic import GameState
 
# ── minimal stubs so game_tree.py works standalone ──────────────────────────
MIN_LENGTH = 2
MAX_LENGTH = 20

class GameTreeNode:
    """One node in the game tree."""
 
    def __init__(self, state: GameState, move_info=None, depth=0):
        self.state     = state
        self.move_info = move_info   # dict: {index, pair, new_symbol, player}
        self.depth     = depth
        self.children  = []         # list[GameTreeNode]
 
    # ── pretty helpers ────────────────────────────────────────────────────────
    def sequence_str(self):
        return "[" + ", ".join(str(x) for x in self.state.sequence) + "]"
 
    def scores_str(self):
        s = self.state.scores
        return f"P1={s[0]:+d}  P2={s[1]:+d}"
 
    def label(self):
        if self.move_info is None:
            return f"ROOT  seq={self.sequence_str()}  {self.scores_str()}"
        mi = self.move_info
        return (
            f"[D{self.depth}] {mi['player']} picks pair '{mi['pair']}' "
            f"@ idx {mi['index']} → '{mi['new_symbol']}'  "
            f"seq={self.sequence_str()}  {self.scores_str()}"
        )
 
 
# ── tree builder ──────────────────────────────────────────────────────────────
 
def build_game_tree(state: GameState, max_depth: int = 3) -> GameTreeNode:
    """
    Recursively build the game tree up to *max_depth* plies deep.
 
    Parameters
    ----------
    state     : the *current* GameState (will NOT be mutated)
    max_depth : how many plies (half-moves) to expand
 
    Returns
    -------
    GameTreeNode – root of the tree
    """
    root = GameTreeNode(state=copy.deepcopy(state), depth=0)
    _expand(root, max_depth)
    return root
 
 
def _expand(node: GameTreeNode, remaining: int):
    if remaining == 0 or node.state.is_game_over():
        return
 
    for idx, pair in node.state.get_available_pairs():
        # deep-copy so each branch is independent
        child_state = copy.deepcopy(node.state)
        child_state.apply_move(idx)
 
        move_info = {
            "player":     node.state.player_names[node.state.current_player],
            "index":      idx,
            "pair":       pair,
            "new_symbol": child_state.sequence[idx],   # symbol that replaced the pair
        }
 
        child_node = GameTreeNode(
            state=child_state,
            move_info=move_info,
            depth=node.depth + 1,
        )
        node.children.append(child_node)
        _expand(child_node, remaining - 1)
 
 
# ── pretty-print ──────────────────────────────────────────────────────────────
 
def print_tree(node: GameTreeNode, prefix: str = "", is_last: bool = True):
    connector = "└── " if is_last else "├── "
    print(prefix + (connector if node.depth > 0 else "") + node.label())

    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node.children):
        print_tree(child, child_prefix, i == len(node.children) - 1)
 
 
# ── statistics ────────────────────────────────────────────────────────────────
 
def tree_stats(node: GameTreeNode):
    total, leaves, by_depth = [0], [0], {}
 
    def walk(n):
        total[0] += 1
        by_depth[n.depth] = by_depth.get(n.depth, 0) + 1
        if not n.children:
            leaves[0] += 1
        for c in n.children:
            walk(c)
 
    walk(node)
    return {"total": total[0], "leaves": leaves[0], "by_depth": by_depth}


