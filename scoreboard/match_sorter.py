from enum import Enum


class MatchSorter(Enum):
    GOALS_TOTAL = lambda m: (-m.total_score, -m.order_started)
    ALPHANUMERIC_HOME_TEAM = lambda m: (m.home, -m.order_started)
