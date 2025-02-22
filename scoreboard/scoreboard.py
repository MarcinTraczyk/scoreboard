from typing import Dict, List, Tuple
from .match import Match
from .match_sorter import MatchSorter


class Scoreboard:
    def __init__(self):
        # A dict to store all ongoing matches.
        self.matches: Dict[str, Match] = {}
        # A list of teams that
        self.teams: List[str] = set()
        self.order_counter: int = 0
        self._home_color = '\x1b[5;30;46m'
        self._away_color = '\x1b[6;30;42m'
        self._color_end = '\x1b[0m'

    def _team_names_to_key(self, home_team: str, away_team: str) -> str:
        """Return a dictionary key for a match, based on home / away team names,
        to use in the self.matches dictionary.

        Args:
            home_team (str): Home team name.
            away_team (str): Away team name

        Returns:
            str: A string key to be used in the self.matches dict.
        """
        return f"{home_team.lower()}_{away_team.lower()}"
    
    def __len__(self):
        return len(self.matches)

    def start_match(self, home_team: str, away_team: str):
        m = Match(home=home_team, away=away_team)
        key = self._team_names_to_key(home_team, away_team)

        if home_team.lower() in self.teams or away_team.lower() in self.teams:
            # Does it make sense to return different error messages in scenarios?
            # (1) both teams already playing
            # (2) the exact match is already on the scoreboard
            # (3) only one of the teams is already playing
            # At this moment these scenarios are covered with a single exception.
            raise ValueError("At least one of the teams is in an active scoreboard game already.")

        m.order_started = self.order_counter
        self.order_counter += 1
        self.teams.add(home_team.lower())
        self.teams.add(away_team.lower())

        self.matches[key] = m

    def get_match(self, team_a: str, team_b: str, order_sensitive: bool=False) -> Match:
        
        # Look for key in the match dictionary.
        key = self._team_names_to_key(team_a, team_b)
        if key in self.matches:
            return self.matches[key]
        
        # In an order-sensitive case, raise an exception on a key not found.
        if order_sensitive:
            raise ValueError("Match does not exist on the scoreboard.")
        
        # In an order-insensitive case, repeat the search in the reversed home / away order.
        return self.get_match(team_a=team_b, team_b=team_a, order_sensitive=True)
    
    def update_match_score(self, home_team: str, away_team: str, home_score: int, away_score: int):
        m = self.get_match(team_a=home_team, team_b=away_team, order_sensitive=True)
        m.home_score = home_score
        m.away_score = away_score

    def finish_match(self, team_a: str, team_b: str, order_sensitive:bool = False):
        # Look for key in the match dictionary.
        key = self._team_names_to_key(team_a, team_b)
        if key in self.matches:
            del self.matches[key]
            self.teams.remove(team_a.lower())
            self.teams.remove(team_b.lower())
            return
        
        # In an order-sensitive case, raise an exception on a key not found.
        if order_sensitive:
            raise ValueError("Match does not exist on the scoreboard.")
        
        # In an order-insensitive case, repeat the search in the reversed home / away order.
        return self.finish_match(team_a=team_b, team_b=team_a, order_sensitive=True)

    def sort_matches(self, sorter: MatchSorter = MatchSorter.GOALS_TOTAL) -> List[Match]:
        return sorted(self.matches.values(), key=sorter)
    
    def _get_matches_for_summary(self, max_lines: int, start_from: int) -> Tuple[List[Match], bool]:
        ordered_matched = self.sort_matches()
        
        if len(self) + start_from <= max_lines:
            add_ellipsis = False
            matches_to_print = ordered_matched[start_from:]
        else:
            if start_from + max_lines < len(ordered_matched):
                add_ellipsis = True
            else:
                add_ellipsis = False
            matches_to_print = ordered_matched[start_from:start_from+max_lines]

        return matches_to_print, add_ellipsis

    def _basic_match_printer(self, match: Match, column_width: int):
        match_line = f"{match.home:<{column_width}} {match.home_score:02d}:"
        match_line += f"{match.away_score:02d} {match.away:>{column_width}}\n"
        return match_line
    
    def _pretty_match_printer(self, match: Match, column_width: int):
        match_line = self._home_color + f"{match.home:<{column_width}} {match.home_score:02d}" + self._color_end
        match_line += ":"
        match_line += self._away_color + f"{match.away_score:02d} {match.away:>{column_width}}" + self._color_end
        match_line += "\n"
        return match_line

    def _get_column_width(self, matches: List[Match], padding=5) -> int:
        max_home_name_length = max((len(match.home) for match in matches), default=0)
        max_away_name_length = max((len(match.away) for match in matches), default=0)
        return max([max_home_name_length, max_away_name_length]) + padding
    
    def _get_summary_header(self, column_width: int) -> str:
        home_header = "HOME"
        away_header = "AWAY"
        header_line = self._home_color + f"{home_header:<{column_width}}   " + self._color_end + "|"
        header_line += self._away_color + f"   {away_header:>{column_width}}" + self._color_end + "\n"
        header_line += "-" * (2 * column_width + 7) + "\n"
        return header_line
    
    def _get_summary_footer(self, column_width: int) -> str:
        return "-" * (2 * column_width + 7) + "\n"

    def summary(self, pretty=False, max_lines=20, start_from=0) -> str:
        summary_string = ""

        matches, ellipsis = self._get_matches_for_summary(max_lines, start_from)
        col_width = self._get_column_width(matches)
        if pretty:
            summary_string += self._get_summary_header(col_width)
        for m in matches:
            if pretty:
                summary_string += self._pretty_match_printer(m, col_width)
            else:
                summary_string += self._basic_match_printer(m, col_width)
        
        if ellipsis:
            summary_string += "(...)\n"
        if pretty:
            summary_string += self._get_summary_footer(col_width)
        return summary_string
        
        

