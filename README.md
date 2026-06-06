# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**

The game is a simple number guessing game built in Streamlit. The app picks a
secret number based on the difficulty you choose, and you try to guess it before
you run out of attempts. After each guess it gives you a hint (go higher or go
lower), tracks your score, and keeps a history of your guesses in the debug
window. The whole point of this project was that an AI built it and left a bunch
of bugs in it, so my job was to play it, find whats broken, and fix it.

- [x] **Detail which bugs you found.**

Here are the bugs i found (i sorted them into code bugs and logic bugs):

- _New Game only reset the secret number_ — the score, attempts, and history all stayed the same so it never felt like a fresh game.
- _History was delayed by 1_ — the debug window always showed my previous guess instead of the one i just made.
- _Secret was made before a difficulty was picked_ — so the number could be outside the range after you switched difficulty.
- _Hints were backwards_ — "Too High" told me to go HIGHER and "Too Low" told me to go LOWER, the complete opposite.
- _Attempts left didn't match attempts allowed_ — it started one short, and later i found it also lagged a guess behind during play.
- _Score went into the negatives_ and also flip-flopped (gave points then took them right back on the next guess).
- _Hard was easier than Normal_ — Hard had the fewest attempts but the smallest range, which didnt make sense.

- [x] **Explain what fixes you applied.**

- **New Game** now resets _everything_ (attempts, score, status, history) and makes a new secret inside the current difficulty's range.
- **History delay** was because Streamlit re-runs top to bottom and the debug window drew the history before my new guess got added. I used an `st.empty()` placeholder and fill it _after_ the guess is processed.
- **Secret range** — i track which difficulty the secret was made for, and if you switch difficulty it starts a fresh round with a new secret in the right range.
- **Hints** — fixed the directions so Too High says go LOWER and Too Low says go HIGHER, and removed a sneaky bug that turned the secret into a string every other turn.
- **Attempts left** — the counter now starts at 0 (counts guesses actually made), and i render the info box with a placeholder so it doesnt lag behind.
- **Score** — scrapped the confusing logic for a simple rule: closer guess = +5, farther = -5, and it cant go below 0.
- **Difficulty** — gave Hard the widest range (1-200) so with the fewest attempts it's genuinely the hardest.
- **Refactor + tests** — moved the game logic into `logic_utils.py` and got all the `pytest` tests passing (plus added 2 of my own).

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range **1–100**, **8** attempts). The
secret number is **50** (visible in the "Developer Debug Info" expander). Scoring
is simple: a guess that lands **closer** to the secret than your last one earns
**+5**, a guess that lands **farther** loses **5**, and the score never drops
below **0**.

1. The game loads on Normal. The info box reads _"Guess a number between 1 and 100. Attempts left: 8"_ — the count matches the attempts allowed.
2. User enters **40** → _"📈 Go HIGHER!"_ (Too Low). This is the first guess, so the score stays at **0**. Attempts left: **7**.
3. User enters **45** → _"📈 Go HIGHER!"_ (Too Low). 45 is closer to 50 than 40 was, so the score goes **+5 → 5**. Attempts left: **6**.
4. User enters **70** → _"📉 Go LOWER!"_ (Too High). 70 is farther away, so the score would go −5 but is floored, landing at **0**. Attempts left: **5**.
5. User enters **48** → _"📈 Go HIGHER!"_ (Too Low). 48 is closer than 70, so the score goes **+5 → 5**. Attempts left: **4**.
6. User enters **50** → _"🎉 Correct!"_ The balloons fire and the game shows _"You won! The secret was 50. Final score: 5"_.
7. Clicking **New Game 🔁** resets everything — attempts back to 8, score to 0, and the history/log cleared — and generates a fresh secret.
8. Switching the difficulty (e.g. to **Easy**) immediately starts a new round with a secret inside that difficulty's range (Easy 1–20, Normal 1–100, Hard 1–200), so the number to guess is always reachable.

**Screenshot** _(optional)_: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.0, pytest-9.0.2, pluggy-1.6.0
collected 5 items

tests/test_game_logic.py .....                                           [100%]

============================== 5 passed in 0.04s ===============================
```

The 5 tests cover the starter hint checks (`Win`, `Too High`, `Too Low`) plus
two added for fixed bugs: the score never going negative, and Hard's range
being at least as wide as Normal's.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
