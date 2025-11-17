"""Core game logic for Tic Tac Toe: board, moves, winner detection, and simple AI."""

from __future__ import annotations
from typing import List, Optional, Tuple
import random

# Type aliases
Board = List[Optional[str]]

# Constant winning lines (0-based indices)
WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


# PUBLIC_INTERFACE
def reset_board() -> Board:
    """Return a fresh empty 3x3 board represented as a list of 9 entries (None)."""
    return [None] * 9


# PUBLIC_INTERFACE
def available_moves(board: Board) -> List[int]:
    """Return a list of indices that are currently empty on the board."""
    return [i for i, v in enumerate(board) if v is None]


# PUBLIC_INTERFACE
def make_move(board: Board, player: str, pos: int) -> bool:
    """Attempt to place player's mark ('X' or 'O') at position pos (0-8).
    Returns True if the move is made, False if invalid.
    """
    if player not in ("X", "O"):
        return False
    if pos < 0 or pos > 8:
        return False
    if board[pos] is not None:
        return False
    board[pos] = player
    return True


# PUBLIC_INTERFACE
def check_winner(board: Board) -> Tuple[Optional[str], Optional[Tuple[int, int, int]]]:
    """Check if there is a winner.
    Returns (winner, winning_line) where:
      - winner is 'X' or 'O' if someone won, else None
      - winning_line is the tuple of indices forming the win if any
    """
    for a, b, c in WIN_LINES:
        va, vb, vc = board[a], board[b], board[c]
        if va is not None and va == vb == vc:
            return va, (a, b, c)
    return None, None


# PUBLIC_INTERFACE
def is_draw(board: Board) -> bool:
    """Return True if the game is a draw (no winner and no moves left)."""
    winner, _ = check_winner(board)
    return winner is None and all(v is not None for v in board)


# PUBLIC_INTERFACE
def ai_move(board: Board, ai_player: str = "O") -> Optional[int]:
    """Simple easy AI: pick a random available move.
    Returns the chosen index, or None if no moves available.
    """
    moves = available_moves(board)
    if not moves:
        return None
    choice = random.choice(moves)
    make_move(board, ai_player, choice)
    return choice
