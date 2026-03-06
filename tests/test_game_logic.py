from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# ---------- get_range_for_difficulty ----------

def test_easy_difficulty_returns_1_to_20():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_difficulty_returns_1_to_100():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_hard_difficulty_returns_1_to_200():
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_unknown_difficulty_falls_back_to_normal_range():
    assert get_range_for_difficulty("Extreme") == (1, 100)


def test_empty_string_difficulty_falls_back_to_normal_range():
    assert get_range_for_difficulty("") == (1, 100)


def test_lowercase_difficulty_falls_back_to_normal_range():
    # The function uses exact match, so "easy" != "Easy"
    assert get_range_for_difficulty("easy") == (1, 100)


# ---------- parse_guess ----------

def test_parse_guess_with_none_input():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


def test_parse_guess_with_empty_string():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


def test_parse_guess_with_non_numeric_string():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."


def test_parse_guess_with_special_characters():
    ok, value, error = parse_guess("!@#")
    assert ok is False
    assert value is None
    assert error == "That is not a number."


def test_parse_guess_with_valid_integer_string():
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None


def test_parse_guess_with_negative_integer():
    ok, value, error = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert error is None


def test_parse_guess_with_float_string_truncates_to_int():
    ok, value, error = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert error is None


def test_parse_guess_with_float_string_rounds_down():
    ok, value, error = parse_guess("9.99")
    assert ok is True
    assert value == 9
    assert error is None


def test_parse_guess_in_range_when_bounds_provided():
    ok, value, error = parse_guess("50", low=1, high=100)
    assert ok is True
    assert value == 50
    assert error is None


def test_parse_guess_at_lower_bound():
    ok, value, error = parse_guess("1", low=1, high=100)
    assert ok is True
    assert value == 1
    assert error is None


def test_parse_guess_at_upper_bound():
    ok, value, error = parse_guess("100", low=1, high=100)
    assert ok is True
    assert value == 100
    assert error is None


def test_parse_guess_below_lower_bound():
    ok, value, error = parse_guess("0", low=1, high=100)
    assert ok is False
    assert value is None
    assert error == "Guess must be between 1 and 100."


def test_parse_guess_above_upper_bound():
    ok, value, error = parse_guess("101", low=1, high=100)
    assert ok is False
    assert value is None
    assert error == "Guess must be between 1 and 100."


def test_parse_guess_no_range_check_when_only_low_provided():
    # Range check only applies when both low and high are given
    ok, value, error = parse_guess("0", low=1)
    assert ok is True
    assert value == 0
    assert error is None


def test_parse_guess_no_range_check_when_only_high_provided():
    ok, value, error = parse_guess("999", high=100)
    assert ok is True
    assert value == 999
    assert error is None


# ---------- check_guess ----------

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_guess_one_above_secret():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"


def test_guess_one_below_secret():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"


def test_check_guess_with_negative_numbers():
    outcome, _ = check_guess(-10, -5)
    assert outcome == "Too Low"


def test_check_guess_with_zero():
    outcome, _ = check_guess(0, 0)
    assert outcome == "Win"


# ---------- update_score ----------

def test_win_on_first_attempt_adds_80_points():
    # attempt_number=0 -> points = 100 - 10*(0+1) = 90
    assert update_score(0, "Win", 0) == 90


def test_win_on_second_attempt_adds_80_points():
    # attempt_number=1 -> points = 100 - 10*(1+1) = 80
    assert update_score(0, "Win", 1) == 80


def test_win_on_ninth_attempt_gives_minimum_10_points():
    # attempt_number=8 -> points = 100 - 10*(8+1) = 10
    assert update_score(0, "Win", 8) == 10


def test_win_on_late_attempt_clamps_to_minimum_10_points():
    # attempt_number=10 -> points = 100 - 10*(10+1) = -10, clamped to 10
    assert update_score(0, "Win", 10) == 10


def test_win_adds_to_existing_score():
    assert update_score(50, "Win", 1) == 130  # 50 + 80


def test_too_high_subtracts_5_points():
    assert update_score(100, "Too High", 1) == 95


def test_too_low_subtracts_5_points():
    assert update_score(100, "Too Low", 1) == 95


def test_too_high_can_make_score_negative():
    assert update_score(2, "Too High", 1) == -3


def test_too_low_can_make_score_negative():
    assert update_score(0, "Too Low", 1) == -5


def test_unknown_outcome_returns_score_unchanged():
    assert update_score(50, "Unknown", 1) == 50


def test_empty_outcome_returns_score_unchanged():
    assert update_score(50, "", 1) == 50
