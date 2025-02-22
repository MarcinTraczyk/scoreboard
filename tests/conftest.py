import pytest
from scoreboard.match import Match


@pytest.fixture
def sample_match():
    """Returns a single Match instance."""
    return Match(home="Team A", away="Team B")


@pytest.fixture
def sample_matches():
    """Returns a Match instances."""
    return [
        Match(home="Team A", away="Team B"),
        Match(home="Team C", away="Team D"),
        Match(home="Team E", away="Team F"),
        Match(home="Team G", away="Team H"),
        Match(home="Team I", away="Team J"),
    ]
