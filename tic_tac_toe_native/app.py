"""Streamlit Tic Tac Toe application with Ocean Professional theme.

This app supports:
- Player vs Player and Player vs Computer (easy AI)
- Scoreboard tracking (X wins, O wins, Draws)
- Move history with (row, col)
- Highlighted winning line
- New Game and Reset Scores actions

Run:
  streamlit run tic_tac_toe_native/app.py
"""

from __future__ import annotations
from typing import List, Optional, Tuple, Dict

import os
import streamlit as st

from .game import (
    reset_board,
    available_moves,
    make_move,
    check_winner,
    is_draw,
    ai_move,
)
from .utils import PLAYER_X, PLAYER_O, GAME_MODES, coord_from_index, format_badge


def _init_session_state() -> None:
    """Initialize all required keys in st.session_state."""
    if "board" not in st.session_state:
        st.session_state.board = reset_board()
    if "current_player" not in st.session_state:
        st.session_state.current_player = PLAYER_X
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "winner" not in st.session_state:
        st.session_state.winner = None  # type: Optional[str]
    if "winning_line" not in st.session_state:
        st.session_state.winning_line = None  # type: Optional[Tuple[int,int,int]]
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = GAME_MODES[0]
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "D": 0}  # type: Dict[str, int]
    if "move_history" not in st.session_state:
        st.session_state.move_history = []  # list of (player, idx, (r,c))


def _start_new_game() -> None:
    """Reset only the board and game status, keep scores."""
    st.session_state.board = reset_board()
    st.session_state.current_player = PLAYER_X
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = None
    st.session_state.move_history = []


def _apply_move(idx: int, player: str) -> bool:
    """Apply a move for player at idx and update state; return True if move made."""
    moved = make_move(st.session_state.board, player, idx)
    if moved:
        r, c = coord_from_index(idx)
        st.session_state.move_history.append((player, idx, (r, c)))
    return moved


def _post_move_evaluate_and_toggle() -> None:
    """After a move, evaluate win/draw and toggle player turn if game continues."""
    winner, line = check_winner(st.session_state.board)
    if winner:
        st.session_state.game_over = True
        st.session_state.winner = winner
        st.session_state.winning_line = line
        st.session_state.scores[winner] += 1
        return

    if is_draw(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = None
        st.session_state.winning_line = None
        st.session_state.scores["D"] += 1
        return

    # Toggle
    st.session_state.current_player = PLAYER_O if st.session_state.current_player == PLAYER_X else PLAYER_X


def _computer_turn_if_needed() -> None:
    """Execute computer move if in PvC mode and it's O's turn and game not over."""
    if st.session_state.game_mode != "Player vs Computer":
        return
    if st.session_state.game_over:
        return
    if st.session_state.current_player != PLAYER_O:
        return

    # AI always plays as O in this simple version
    chosen = ai_move(st.session_state.board, ai_player=PLAYER_O)
    if chosen is not None:
        r, c = coord_from_index(chosen)
        st.session_state.move_history.append((PLAYER_O, chosen, (r, c)))
        _post_move_evaluate_and_toggle()


def _render_header_and_actions() -> None:
    st.markdown('<div class="tictactoe-container">', unsafe_allow_html=True)
    st.markdown('<div class="header-strip"></div>', unsafe_allow_html=True)
    st.title("Tic Tac Toe")
    st.markdown('<p class="ttt-subtitle">Ocean Professional • Modern UI</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("New Game", help="Start a new round", type="primary"):
            _start_new_game()
    with col_b:
        if st.button("Reset Scores", help="Reset X/O/Draw counters", type="secondary"):
            st.session_state.scores = {"X": 0, "O": 0, "D": 0}
            _start_new_game()


def _render_scoreboard() -> None:
    s = st.session_state.scores
    x_card, d_card, o_card = st.columns(3)
    with x_card:
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown('<div class="score-title">X Wins</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-value" style="color:#2563EB">{s["X"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with d_card:
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown('<div class="score-title">Draws</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-value" style="color:#6B7280">{s["D"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with o_card:
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown('<div class="score-title">O Wins</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-value" style="color:#F59E0B">{s["O"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def _render_status_badges() -> None:
    b = []
    if st.session_state.game_over:
        if st.session_state.winner:
            b.append(format_badge(f"Winner: {st.session_state.winner}", "success"))
        else:
            b.append(format_badge("Game is a draw", "muted"))
    else:
        b.append(format_badge(f"Turn: {st.session_state.current_player}", "info"))

    if st.session_state.winning_line:
        b.append(format_badge(f"Winning line: {st.session_state.winning_line}", "success"))

    st.markdown('<div class="badge-row">' + "".join(b) + "</div>", unsafe_allow_html=True)


def _cell_label(value: Optional[str], idx: int) -> str:
    """Accessible label for buttons."""
    r, c = coord_from_index(idx)
    if value is None:
        return f"Cell ({r+1},{c+1}) empty"
    return f"Cell ({r+1},{c+1}) {value}"


def _render_grid() -> None:
    win_line = set(st.session_state.winning_line) if st.session_state.winning_line else set()
    for row in range(3):
        cols = st.columns(3, gap="small")
        for col in range(3):
            idx = row * 3 + col
            value = st.session_state.board[idx]
            disabled = value is not None or st.session_state.game_over

            # Style classes
            classes = ["cell-btn"]
            if value == PLAYER_X:
                classes.append("cell-x")
            elif value == PLAYER_O:
                classes.append("cell-o")
            if idx in win_line:
                classes.append("cell-win")

            # Render button
            with cols[col]:
                btn_key = f"cell_{idx}"
                label = value if value is not None else " "
                clicked = st.button(
                    label,
                    key=btn_key,
                    help=_cell_label(value, idx),
                    disabled=disabled,
                    use_container_width=True,
                )
                # Apply custom classes via HTML wrapper to preserve styling
                st.markdown(
                    f"""
                    <style>
                    div[data-testid="baseButton-secondary"][data-testid="stButton"] button#{btn_key} {{
                        display:none !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                # Recreate visual button (click captured above)
                st.markdown(
                    f'<button class="{" ".join(classes)}" aria-label="{_cell_label(value, idx)}" disabled></button>',
                    unsafe_allow_html=True,
                )

                if clicked and not disabled:
                    _on_human_click(idx)


def _on_human_click(idx: int) -> None:
    if st.session_state.game_over:
        return
    current = st.session_state.current_player
    if not _apply_move(idx, current):
        return
    _post_move_evaluate_and_toggle()
    # Computer move if applicable
    _computer_turn_if_needed()


def _render_move_history() -> None:
    st.markdown('<div class="move-history">', unsafe_allow_html=True)
    st.markdown("#### Move History")
    if not st.session_state.move_history:
        st.caption("No moves yet.")
    else:
        for i, (player, idx, (r, c)) in enumerate(st.session_state.move_history, start=1):
            st.markdown(f'<div class="move-item">#{i} • {player} → ({r+1},{c+1}) [idx {idx}]</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    """Entry point for the Streamlit app."""
    st.set_page_config(
        page_title="Tic Tac Toe",
        page_icon="🎮",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Load theme
    theme_path = os.path.join(os.path.dirname(__file__), "theme.css")
    try:
        with open(theme_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

    _init_session_state()

    # Sidebar
    with st.sidebar:
        st.header("Game Settings")
        mode = st.selectbox("Mode", GAME_MODES, index=0)
        if mode != st.session_state.game_mode:
            st.session_state.game_mode = mode
            _start_new_game()

        st.markdown("---")
        st.subheader("About")
        st.write(
            "A minimal, modern Tic Tac Toe built with Streamlit. "
            "Ocean Professional theme with blue and amber accents."
        )

    # Header and actions
    _render_header_and_actions()
    _render_scoreboard()
    _render_status_badges()

    # Grid
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    _render_grid()
    st.markdown("</div>", unsafe_allow_html=True)

    # Move history
    _render_move_history()

    # Close container wrapper
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
