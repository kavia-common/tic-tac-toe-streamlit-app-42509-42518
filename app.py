import streamlit as st

# PUBLIC_INTERFACE
def main():
    """Minimal Streamlit app to verify environment and startup.
    
    Renders a basic page with a title and note that the full Tic Tac Toe game
    will be implemented in subsequent steps.
    """
    st.set_page_config(page_title="Tic Tac Toe (Bootstrap)", page_icon="🎮", layout="centered")
    # Apply a light "Ocean Professional" vibe with Streamlit primitives
    st.markdown(
        """
        <style>
            .app-header {
                font-size: 2.0rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.25rem;
            }
            .app-sub {
                color: #374151;
                margin-bottom: 1.0rem;
            }
            .card {
                background: #ffffff;
                border-radius: 12px;
                padding: 1.2rem 1rem;
                box-shadow: 0 2px 10px rgba(37, 99, 235, 0.08);
                border: 1px solid rgba(37, 99, 235, 0.08);
            }
            .badge {
                display: inline-block;
                font-size: 0.85rem;
                background: #EFF6FF;
                color: #2563EB;
                padding: 0.2rem 0.5rem;
                border-radius: 8px;
                margin-top: 0.25rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="app-header">Tic Tac Toe</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-sub">Streamlit Native Container • Bootstrap Check</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.success("Environment bootstrap successful. The app is running.")
        st.write(
            "This is a minimal placeholder to verify that dependencies install and "
            "Streamlit can start. The full game implementation will follow."
        )
        st.markdown('<span class="badge">Status: Ready for game logic</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Tip: The platform will inject the PORT; no changes are needed.")


if __name__ == "__main__":
    main()
