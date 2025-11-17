"""Utility helpers and constants for the Tic Tac Toe Streamlit app."""

from typing import Tuple

# Players
PLAYER_X = "X"
PLAYER_O = "O"

GAME_MODES = ("Player vs Player", "Player vs Computer")


def coord_from_index(idx: int) -> Tuple[int, int]:
    """Convert linear index [0..8] to (row, col) where row, col in [0..2]."""
    return divmod(idx, 3)


def format_badge(text: str, kind: str = "info") -> str:
    """Return an HTML status badge with theme-aligned colors.
    kind: 'info' (primary), 'success' (amber), 'error' (red), 'muted'
    """
    colors = {
        "info": "#2563EB",
        "success": "#F59E0B",
        "error": "#EF4444",
        "muted": "#6B7280",
    }
    color = colors.get(kind, colors["info"])
    return f'''
    <span class="ttt-badge" style="
        display:inline-block;
        padding:4px 10px;
        border-radius:9999px;
        background:{color}1A;
        color:{color};
        font-weight:600;
        font-size:0.85rem;
        border:1px solid {color}33;
    ">{text}</span>
    '''
