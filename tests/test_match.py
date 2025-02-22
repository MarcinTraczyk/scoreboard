import pytest
from scoreboard.match import Match
from pydantic import ValidationError


invalid_scores = [
    (-1, "negative value"),
    ("foo", "string value"),
    (456789, "excessively large score"),  # score cannot be too large (largest score ever was about 150 goals)
    (4.5, "float score"),
]


def test_initial_score_is_zero(sample_match):
    assert sample_match.away_score == 0
    assert sample_match.home_score == 0


def test_home_away_name_assigned_correctly(sample_match):
    assert sample_match.home == 'Team A'
    assert sample_match.away == "Team B"


@pytest.mark.parametrize("invalid_score, description", invalid_scores,
                         ids=[desc for _, desc in invalid_scores])
def test_invalid_home_score_raise_exception(invalid_score, description, sample_match):
    with pytest.raises(ValidationError):
        sample_match.home_score = invalid_score


@pytest.mark.parametrize("invalid_score, description", invalid_scores,
                         ids=[desc for _, desc in invalid_scores])
def test_invalid_away_score_raise_exception(invalid_score, description, sample_match):
    with pytest.raises(ValidationError):
        sample_match.away_score = invalid_score


@pytest.mark.parametrize("home_score", "away_score", "total_score", [
    (0, 0, 0),
    (1, 1, 2),
    (0, 3, 3),
    (10, 10, 20)
])
def test_total_scores(home_score, away_score, total_score, sample_match):
    sample_match.home_score = home_score
    sample_match.away_score = away_score
    assert sample_match.total_score == total_score
