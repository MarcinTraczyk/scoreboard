import pytest
from scoreboard.scoreboard import Scoreboard
from scoreboard.match_sorter import MatchSorter
from scoreboard.match import Match


def test_initial_scoreboard_is_empty(sample_scoreboard):
    """Ensure the newly instantiated scoreboard is empty."""
    assert len(sample_scoreboard) == 0


def test_start_single_match(sample_scoreboard):
    """Verify a match can be started, looking at the length of scoreboard."""
    sample_scoreboard.start_match("Team A", "Team B")
    assert len(sample_scoreboard) == 1


def test_start_multiple_matches(sample_scoreboard):
    """Verify multiple matches can be started, looking at the length of scoreboard."""
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")

    assert len(sample_scoreboard) == 10


def test_cannot_start_same_match_twice(sample_scoreboard):
    """Ensure a match between the two same teams cannot be added twice."""
    sample_scoreboard.start_match("Team A", "Team B")
    with pytest.raises(ValueError):
        sample_scoreboard.start_match("Team A", "Team B")


def test_cannot_start_match_for_a_home_team_already_playing(sample_scoreboard):
    """Verify the home team cannot play in two matches simultaneously."""
    sample_scoreboard.start_match("Team A", "Team B")
    with pytest.raises(ValueError):
        sample_scoreboard.start_match("Team C", "Team B")


def test_cannot_start_match_for_an_away_team_already_playing(sample_scoreboard):
    """Verify the away team cannot play in two matches simultaneously."""
    sample_scoreboard.start_match("Team A", "Team B")
    with pytest.raises(ValueError):
        sample_scoreboard.start_match("Team A", "Team C")


@pytest.mark.parametrize(("home_team", "away_team"), [
    ("team a", "Team B"),
    ("Team A", "team b"),
    ("teAm A", "teAM b"),
])
def test_team_name_capitalization_is_normalized_in_the_scoreboard(home_team, away_team, sample_scoreboard):
    """Verify the away team cannot play in two matches simultaneously. Test case insensitivity."""
    sample_scoreboard.start_match(home_team, away_team)
    with pytest.raises(ValueError):
        sample_scoreboard.start_match(home_team, away_team)


def test_get_match(sample_scoreboard):
    """Verify that a correct match is returned."""
    home_name = "Team A"
    away_name = "Team B"
    sample_scoreboard.start_match(home_name, away_name)
    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home == home_name
    assert returned_match.away == away_name


def test_get_match_in_reverse_order(sample_scoreboard):
    """Verify that a correct match is returned, when teams are queried in the reversed order:
      (home/away is queried as away/home)."""
    home_name = "Team A"
    away_name = "Team B"
    sample_scoreboard.start_match(home_name, away_name)
    returned_match = sample_scoreboard.get_match(away_name, home_name)
    assert returned_match.home == home_name
    assert returned_match.away == away_name


def test_get_match_from_longer_collection(sample_scoreboard):
    """Verify that a correct match is returned when 10 matches are present in the scoreboard"""
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")
    home_name = "Team A5"
    away_name = "Team B5"
    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home == home_name
    assert returned_match.away == away_name


def test_get_match_from_longer_collection_using_inconsistent_order(sample_scoreboard):
    """Verify that a correct match is returned when 10 matches are present in the scoreboard,
    when teams are queried in the reversed order: (home/away is queried as away/home)."""
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")
    home_name = "Team A5"
    away_name = "Team B5"
    returned_match = sample_scoreboard.get_match(away_name, home_name)
    assert returned_match.home == home_name
    assert returned_match.away == away_name


def test_get_match_from_longer_collection_using_inconsistent_name_capitalization(sample_scoreboard):
    """Verify that a correct match is returned when 10 matches are present in the scoreboard,
    when teams are queried using inconsistent name capitalization."""
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")
    home_name = "Team A5"
    away_name = "Team B5"
    returned_match = sample_scoreboard.get_match(home_name.lower(), away_name.upper())
    assert returned_match.home == home_name
    assert returned_match.away == away_name


def test_initial_score_is_zero(sample_scoreboard):
    """Verify that a match start with a 0:0 score."""
    home_name = "Team A"
    away_name = "Team B"
    sample_scoreboard.start_match(home_name, away_name)
    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home_score == 0
    assert returned_match.away_score == 0


def test_update_match_score(sample_scoreboard):
    """Verify that a match score can be updated."""
    home_name = "Team A"
    away_name = "Team B"
    sample_scoreboard.start_match(home_name, away_name)
    sample_scoreboard.update_match_score(home_name, away_name, 2, 3)

    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home_score == 2
    assert returned_match.away_score == 3


def test_update_match_score_multiple_times(sample_scoreboard):
    """Verify that a match score can be updated multiple times."""
    home_name = "Team A"
    away_name = "Team B"
    sample_scoreboard.start_match(home_name, away_name)
    sample_scoreboard.update_match_score(home_name, away_name, 0, 1)
    sample_scoreboard.update_match_score(home_name, away_name, 1, 1)
    sample_scoreboard.update_match_score(home_name, away_name, 2, 1)
    sample_scoreboard.update_match_score(home_name, away_name, 3, 1)

    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home_score == 3
    assert returned_match.away_score == 1


def test_update_match_score_from_longer_collection(sample_scoreboard):
    """Verify that a match score can be updated when the scoreboard holds 10 matches."""
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")
    home_name = "Team A5"
    away_name = "Team B5"
    sample_scoreboard.update_match_score(
        home_name,
        away_name,
        2,
        0
    )
    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home_score == 2
    assert returned_match.away_score == 0


def test_update_match_score_from_longer_collection_does_not_affect_other_games(sample_scoreboard):
    """Verify that updating a score of a single match, does not affect others."""
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")
    home_name = "Team A5"
    away_name = "Team B5"
    sample_scoreboard.update_match_score(
        home_name,
        away_name,
        2,
        0
    )
    for i in range(10):
        if i == 5:
            continue
        returned_match = sample_scoreboard.get_match(f"Team A{i}", f"Team B{i}")
        assert returned_match.home_score == 0
        assert returned_match.away_score == 0


def test_start_and_finish_single_match(sample_scoreboard):
    """Ensure the match can be finished by looking at the scoreboard length."""
    sample_scoreboard.start_match("Team A", "Team B")
    sample_scoreboard.finish_match("Team A", "Team B")
    assert len(sample_scoreboard) == 0


def test_cannot_finish_non_existing_match(sample_scoreboard):
    """Ensure the match that does not exist in the scoreboard cannot be finished."""
    home_name = "Team A"
    away_name = "Team B"
    sample_scoreboard.start_match(home_name, away_name)
    with pytest.raises(ValueError):
        sample_scoreboard.finish_match("Team C", "Team D")

    assert len(sample_scoreboard) == 1
    returned_match = sample_scoreboard.get_match(home_name, away_name)
    assert returned_match.home == home_name
    assert returned_match.away == away_name


def test_finish_all_matches_from_longer_collection(sample_scoreboard):
    """Verify that a collection of 10 matches can be finished, reverting back to empty scoreboard. """
    for i in range(10):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")

    for i in range(10):
        sample_scoreboard.finish_match(f"Team A{i}", f"Team B{i}")

    assert len(sample_scoreboard) == 0


def test_default_match_ordering(sample_scoreboard):
    """Test the example specificy given in the requirements."""
    sample_scoreboard.start_match("Mexico", "Canada")
    sample_scoreboard.start_match("Spain", "Brazil")
    sample_scoreboard.start_match("Germany", "France")
    sample_scoreboard.start_match("Uruguay", "Italy")
    sample_scoreboard.start_match("Argentina", "Australia")

    sample_scoreboard.update_match_score("Mexico", "Canada", 0, 5)
    sample_scoreboard.update_match_score("Spain", "Brazil", 10, 2)
    sample_scoreboard.update_match_score("Germany", "France", 2, 2)
    sample_scoreboard.update_match_score("Uruguay", "Italy", 6, 6)
    sample_scoreboard.update_match_score("Argentina", "Australia", 3, 1)

    ordered_matches = sample_scoreboard.sort_matches()

    assert ordered_matches[0].home == "Uruguay"
    assert ordered_matches[0].away == "Italy"
    assert ordered_matches[1].home == "Spain"
    assert ordered_matches[1].away == "Brazil"
    assert ordered_matches[2].home == "Mexico"
    assert ordered_matches[2].away == "Canada"
    assert ordered_matches[3].home == "Argentina"
    assert ordered_matches[3].away == "Australia"
    assert ordered_matches[4].home == "Germany"
    assert ordered_matches[4].away == "France"


def test_default_match_ordering_in_summary(sample_scoreboard):
    """Test the example specificy given in the requirements."""
    sample_scoreboard.start_match("Mexico", "Canada")
    sample_scoreboard.start_match("Spain", "Brazil")
    sample_scoreboard.start_match("Germany", "France")
    sample_scoreboard.start_match("Uruguay", "Italy")
    sample_scoreboard.start_match("Argentina", "Australia")

    sample_scoreboard.update_match_score("Mexico", "Canada", 0, 5)
    sample_scoreboard.update_match_score("Spain", "Brazil", 10, 2)
    sample_scoreboard.update_match_score("Germany", "France", 2, 2)
    sample_scoreboard.update_match_score("Uruguay", "Italy", 6, 6)
    sample_scoreboard.update_match_score("Argentina", "Australia", 3, 1)

    summary = sample_scoreboard.summary()
    summary_lines = summary.splitlines()

    assert "Uruguay" in summary_lines[0]
    assert "Italy" in summary_lines[0]
    assert "06:06" in summary_lines[0]
    assert "Spain" in summary_lines[1]
    assert "Brazil" in summary_lines[1]
    assert "10:02" in summary_lines[1]
    assert "Mexico" in summary_lines[2]
    assert "Canada" in summary_lines[2]
    assert "00:05" in summary_lines[2]
    assert "Argentina" in summary_lines[3]
    assert "Australia" in summary_lines[3]
    assert "03:01" in summary_lines[3]
    assert "Germany" in summary_lines[4]
    assert "France" in summary_lines[4]
    assert "02:02" in summary_lines[4]


def test_use_text_ellipsis_in_summary_when_too_long(sample_scoreboard):
    for i in range(1000):
        sample_scoreboard.start_match(f"Team A{i}", f"Team B{i}")

    summary = sample_scoreboard.summary()
    summary_lines = summary.splitlines()

    assert len(summary_lines) == 21
    assert "(...)" in summary_lines[-1]


def test_alphanumeric_match_ordering(sample_scoreboard):
    """Ensure matches are sorted correctly by the home team name in alphanumeric order."""
    sample_scoreboard.start_match("Mexico", "Canada")
    sample_scoreboard.start_match("Spain", "Brazil")
    sample_scoreboard.start_match("Germany", "France")
    sample_scoreboard.start_match("Uruguay", "Italy")
    sample_scoreboard.start_match("Argentina", "Australia")

    sample_scoreboard.update_match_score("Mexico", "Canada", 0, 5)
    sample_scoreboard.update_match_score("Spain", "Brazil", 10, 2)
    sample_scoreboard.update_match_score("Germany", "France", 2, 2)
    sample_scoreboard.update_match_score("Uruguay", "Italy", 6, 6)
    sample_scoreboard.update_match_score("Argentina", "Australia", 3, 1)

    ordered_matches = sample_scoreboard.sort_matches(MatchSorter.ALPHANUMERIC_HOME_TEAM)

    assert ordered_matches[0].home == "Argentina"
    assert ordered_matches[0].away == "Australia"
    assert ordered_matches[1].home == "Germany"
    assert ordered_matches[1].away == "France"
    assert ordered_matches[2].home == "Mexico"
    assert ordered_matches[2].away == "Canada"
    assert ordered_matches[3].home == "Spain"
    assert ordered_matches[3].away == "Brazil"
    assert ordered_matches[4].home == "Uruguay"
    assert ordered_matches[4].away == "Italy"


def test_empty_summary_can_be_returned(sample_scoreboard):
    """Test the example specificy given in the requirements."""
    summary = sample_scoreboard.summary()
    assert summary == ""
