import random
import streamlit as st

# The pure game logic lives in logic_utils.py so it can be unit tested without
# Streamlit. app.py just handles the UI and session state.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

# FIX: the hint direction was reversed. "Too High" told the player to "Go
# HIGHER" and "Too Low" told them to "Go LOWER" -- the opposite of what they
# should do. Collaborated with Claude Code in agent mode: I reported that the
# hints sent me the wrong way, the AI traced it to the swapped messages. The
# outcome now drives the hint text through this map, with the arrows fixed so
# "Too High" tells you to go LOWER and "Too Low" tells you to go HIGHER.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

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

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
    # Remember which difficulty this secret belongs to, so we can tell when the
    # player switches and the secret needs to be regenerated for the new range.
    st.session_state.difficulty = difficulty

# FIX: attempts started at 1 before the player had guessed anything, so
# "Attempts left" (attempt_limit - attempts) was always one short of the
# attempts allowed. Collaborated with Claude Code in agent mode: I pointed out
# the counter was off by one on a fresh game, the AI identified this start value
# as the cause. attempts now counts guesses ACTUALLY made, starting at 0.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Distance (abs(guess - secret)) of the previous guess, so we can tell if the
# next guess gets closer or farther. None until the first guess is made.
if "prev_distance" not in st.session_state:
    st.session_state.prev_distance = None

# FIX: the secret was generated only once on first load using the default
# difficulty's range, and switching difficulty never regenerated it -- so the
# number to guess could be outside the selected range (e.g. 80 while on Easy
# 1-20). Collaborated with Claude Code in agent mode: I described how the secret
# didn't match the range after changing difficulty, the AI suggested tracking
# the difficulty the secret was made for. When it changes we now start a fresh
# round with a new secret inside the new range.
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.prev_distance = None

st.subheader("Make a guess")

# FIX: this message hardcoded "between 1 and 100" even on Easy/Hard, so it lied
# about the range. It also rendered "Attempts left" up here BEFORE the submit
# handler increments attempts further down, so (like the history below) the
# count lagged one rerun behind -- showing the full allowance even after a
# guess. Collaborated with Claude Code in agent mode: the end-to-end run caught
# the lag, the AI applied the same st.empty() placeholder pattern so the info is
# rendered with the real range AND the up-to-date attempt count.
info_placeholder = st.empty()

# LOGIC BREAKS HERE  <-- crime scene: the debug window used to render the
# history right here, BEFORE the new guess was appended further down. Streamlit
# reruns top-to-bottom, so the list was always one rerun behind.
# FIX: reserve a spot with a placeholder now, then fill it AFTER the guess is
# processed (see render_status() calls below) so the history is always current.
# Collaborated with Claude Code in agent mode: I flagged the "history lags by 1"
# bug, the AI explained Streamlit's top-to-bottom rerun model and suggested the
# st.empty() placeholder pattern so the debug window keeps its position.
debug_placeholder = st.empty()


def render_status():
    # Fill the info box and debug window. Called AFTER the guess is processed so
    # both reflect the current attempt count and history, not last rerun's.
    attempts_left = max(0, attempt_limit - st.session_state.attempts)
    info_placeholder.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )
    with debug_placeholder.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: "New Game" used to only reset the secret number (and even that ignored
# the difficulty range, hardcoding 1-100). Collaborated with Claude Code in
# agent mode: I described the bug, the AI pointed out that score, status, and
# history were never cleared, so a "new" game kept the old score/log. We now
# reset every piece of session state to match a fresh start, using the current
# difficulty's range for the new secret.

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.prev_distance = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_status()
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: on even attempts the secret was being cast to a string, which made
        # the int-vs-str comparison in check_guess blow up and fall back to a
        # lexicographic (text) compare -- so every other guess gave a wrong hint.
        # Collaborated with Claude Code in agent mode: the AI spotted this str()
        # cast as the reason the hints only broke on some turns. We now always
        # compare the guess against the secret as an int.
        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)
        message = HINT_MESSAGES[outcome]

        if show_hint:
            st.warning(message)

        # Score by how close this guess is compared to the previous one. The very
        # first guess has nothing to compare against, so it leaves the score alone.
        distance = abs(guess_int - st.session_state.secret)
        if st.session_state.prev_distance is not None:
            is_closer = distance < st.session_state.prev_distance
            st.session_state.score = update_score(
                current_score=st.session_state.score,
                is_closer=is_closer,
            )
        st.session_state.prev_distance = distance

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

# Fill the info box + debug window now that the guess (if any) has been
# processed, so the attempt count and history are current.
render_status()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
