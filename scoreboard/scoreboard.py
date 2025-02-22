from .match import Match
from typing import Dict, List


class Scoreboard:
    def __init__(self):
        self.matches: Dict[str, Match] = {}
        self.teams: List[str] = []
        self.order_counter: int = 0

    def _team_names_to_key(self, home_team: str, away_team: str) -> str:
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
        self.teams += [home_team.lower(), away_team.lower()]

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
            return
        
        # In an order-sensitive case, raise an exception on a key not found.
        if order_sensitive:
            raise ValueError("Match does not exist on the scoreboard.")
        
        # In an order-insensitive case, repeat the search in the reversed home / away order.
        return self.finish_match(team_a=team_b, team_b=team_a, order_sensitive=True)

    

