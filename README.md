# Tic Tac Toe • Streamlit (Ocean Professional)

A simple Tic Tac Toe game implemented with Streamlit featuring a modern, clean "Ocean Professional" look.

## Features

- Player vs Player and Player vs Computer (easy AI)
- Scoreboard: X wins, O wins, and Draws
- Move history showing (row, col) and index
- Winning line highlight
- New Game and Reset Scores actions
- Themed UI with blue and amber accents, rounded corners, subtle shadows, and a gradient header strip

## Getting Started

1. Ensure you have Python 3.9+ and pip installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run tic_tac_toe_native/app.py
   ```

By default Streamlit runs on port 8501. If your orchestrator provides a PORT env variable, Streamlit will honor it when launched via the container's startup script.

## Theme

This app applies the Ocean Professional theme:

- Background: `#f9fafb`
- Surface: `#ffffff`
- Primary: `#2563EB`
- Secondary/Success: `#F59E0B`
- Error: `#EF4444`

UI follows a modern style with subtle shadows, rounded corners, smooth hover transitions, and a thin gradient header strip.

## Project Structure

```
tic-tac-toe-streamlit-app-42509-42518/
├─ tic_tac_toe_native/
│  ├─ app.py
│  ├─ game.py
│  ├─ utils.py
│  └─ theme.css
├─ requirements.txt
└─ README.md
```

## Notes

- App entry point for Streamlit is `tic_tac_toe_native/app.py`.
- The container `startup.sh` uses `PORT` if provided to run Streamlit bound to `0.0.0.0`.
