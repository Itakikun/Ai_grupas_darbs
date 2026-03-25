import copy
from game_logic import GameState

class GameTreeNode:
    """One node in the game tree."""
 
    def __init__(self, state: GameState, move_info=None, depth=0):
        self.state     = state
        self.move_info = move_info   # dict: {index, pair, new_symbol, player}
        self.depth     = depth
        self.children  = []         # list[GameTreeNode]
 
 
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
