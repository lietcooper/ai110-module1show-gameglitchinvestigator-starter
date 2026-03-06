import random
import pandas as pd
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Sidebar metrics (improvement #3)
st.sidebar.divider()
st.sidebar.metric("Score", st.session_state.get("score", 0))
attempts = st.session_state.get("attempts", 0)
st.sidebar.metric("Attempts", f"{attempts}/{attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

st.subheader("Make a guess")

# Bug 2 fix: use dynamic range instead of hardcoded "1 and 100"
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# Progress bar for attempts (improvement #1)
st.progress(st.session_state.attempts / attempt_limit)

# Bug 1 fix: use st.form so Enter key submits the guess
with st.form("guess_form"):
    # Number input instead of text input (improvement #5)
    raw_guess = st.number_input(
        "Enter your guess:",
        min_value=low,
        max_value=high,
        value=low,
        step=1,
        key=f"guess_input_{difficulty}"
    )
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Submit Guess 🚀")
    with col2:
        show_hint = st.checkbox("Show hint", value=True)

new_game = st.button("New Game 🔁")

# Bug 5 fix: reset all session state on new game, use difficulty range
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(str(raw_guess), low, high)

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1

        # Bug 4 fix: always pass int secret (no str() conversion)
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Store guess with outcome (improvement #6)
        st.session_state.history.append({"guess": guess_int, "result": outcome})

        # Color-coded feedback (improvement #4)
        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.error(message)
            else:
                st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Guess history table (improvement #2)
if st.session_state.history:
    st.subheader("Guess History")
    history_df = pd.DataFrame(st.session_state.history)
    history_df.index = range(1, len(history_df) + 1)
    history_df.index.name = "Attempt"
    history_df.columns = ["Guess", "Result"]
    st.table(history_df)

# Bug 3 fix: debug info moved AFTER submit processing so history is up-to-date
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
