def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard used to have the smallest range (1-50) while also having the
    # fewest attempts, which made it easier than Normal. Ranges now grow with
    # difficulty (Easy < Normal < Hard) so Hard is genuinely the hardest.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, is_closer: bool):
    """
    Score by how close the guess is compared to the previous one: +5 if this
    guess is closer to the secret, -5 if it is farther away.
    """
    new_score = current_score + 5 if is_closer else current_score - 5
    # FIX: keep the score from running into negative numbers.
    if new_score < 0:
        new_score = 0
    return new_score
