from logic_utils import check_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_score_never_goes_negative():
    # Targets the "score going into negatives" bug. A farther guess subtracts 5,
    # but starting from 0 the score should floor at 0, not drop to -5.
    result = update_score(0, is_closer=False)
    assert result == 0

def test_hard_range_is_wider_than_normal():
    # Targets the "Hard easier than Normal" bug. Hard has the fewest attempts,
    # so its range must be at least as wide as Normal's to actually be harder.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high >= normal_high
