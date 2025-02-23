from typing import Dict, List, Tuple
from .match import Match
from .match_sorter import MatchSorter
from sys import platform


class Scoreboard:
    MAX_SUMMARY_LINES: int = 20
    COLUMN_PADDING: int = 2
    MIN_COLUMN_WIDTH: int = 10
    MAX_COLUMN_WIDTH: int = 50
    HOME_HEADER: str = "HOME"
    AWAY_HEADER: str = "AWAY"
    TABLE_ELLIPSIS: str = "(...)\n"

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
        """Starts a match between two teams.

        Args:
            home_team (str): Home team name.
            away_team (str): Away team name.

        Raises:
            ValueError: If one of the teams is already in an active scoreboard match, an exception is raised.
            A single team cannot play two games at once.
        """
        m = Match(home=home_team, away=away_team)
        key = self._team_names_to_key(home_team, away_team)

        if home_team.lower() in self.teams or away_team.lower() in self.teams:
            # Does it make sense to return different error messages in scenarios?
            # (1) both teams already playing
            # (2) the exact match is already on the scoreboard
            # (3) only one of the teams is already playing
            # At this moment these scenarios are covered with a single exception.
            raise ValueError("At least one of the teams is in an active scoreboard game already.")

        # Increase the order counter used for secondary sorting.
        m.order_started = self.order_counter
        # In theory we should reset it at some point, but it does not seem like
        # the integer overflow is something we should worry about at this stage.
        self.order_counter += 1

        # Add both teams to the list of teams already engaged in a scoreboard game.
        self.teams.add(home_team.lower())
        self.teams.add(away_team.lower())

        # Add the match instance to the list of active games.
        self.matches[key] = m

    def get_match(self, team_a: str, team_b: str, order_sensitive: bool = False) -> Match:
        """Get an active match, based on team names.

        Args:
            team_a (str): First team name.
            team_b (str): Second team name.
            order_sensitive (bool, optional): Specifies whether the order of teams is important in the query.
                If True, `team_a` is considered the home team and `team_b` the away team. Defaults to False.

        Raises:
            ValueError: Raises a ValueError when queried match is not present on the scoreboard.

        Returns:
            Match: Found match instance.
        """

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
        """Update a selected match score.

        Args:
            home_team (str): Home team name.
            away_team (str): Away team name.
            home_score (int): New home team score.
            away_score (int): New away team score.
        """
        m = self.get_match(team_a=home_team, team_b=away_team, order_sensitive=True)
        m.home_score = home_score
        m.away_score = away_score

    def finish_match(self, team_a: str, team_b: str, order_sensitive: bool = False):
        """Finish an ongoing match.

        Args:
            team_a (str): First team involved in a match.
            team_b (str): Second team involved in a match.
            order_sensitive (bool, optional): Specifies whether the order of teams is important in the query.
                If True, `team_a` is considered the home team and `team_b` the away team. Defaults to False.

        Raises:
            ValueError: Raises a ValueError when queried match is not present on the scoreboard.

        """
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
        """Returns a list of current matches, sorted accoring to one of the rules
        defined in the MatchSorter enum.

        Args:
            sorter (MatchSorter, optional): Sorting rules for a list of match instances.
                Defaults to MatchSorter.GOALS_TOTAL.

        Returns:
            List[Match]: Sorted list of matches.
        """
        return sorted(self.matches.values(), key=sorter)

    def _get_matches_for_summary(self, max_lines: int, start_from: int) -> Tuple[List[Match], bool]:
        """Get a subset of all matches, to be displayed in the summary.

        Args:
            max_lines (int): Max number of matches / lines in the summary to be displayed.
            start_from (int): Index of starting instance in the sorted array of matched.

        Returns:
            Tuple[List[Match], bool]: A subset of matches to summarize and a bool value indicating
                that an ellipsis should be rendered in the summary.
        """
        ordered_matches = self.sort_matches()

        # When there are fewer scoreboard matches than the max number of lines to be
        # displayed in the summary, simply display all requested matches.
        if len(ordered_matches) + start_from <= max_lines:
            add_ellipsis = False
            matches_to_print = ordered_matches[start_from:]
        else:
            # When there's more matches to be displayed than the max number of lines allowed,
            # we display an ellipsis, indicating there's more content available
            if start_from + max_lines < len(ordered_matches):
                add_ellipsis = True
            # The requested range of matches reaches the end of list. Even though the total
            # number of matches stored is larger than the `max_lines` value, we do not show
            # the ellipsis, as the range reaches the end of list.
            else:
                add_ellipsis = False

            matches_to_print = ordered_matches[start_from:start_from+max_lines]

        return matches_to_print, add_ellipsis

    def _match_printer(
        self,
        match: Match,
        column_width: int,
        pretty: bool = False
    ):
        """Add colors to the basic printer function.

        Args:
            match (Match): Match instance to convert to string.
            column_width (int): Column width to use for home / away halves of the string.

        Returns:
            str: A string in a "team A  2:3  team B" format. With two different colors for the home / away halves.
        """
        # We allow for at most 3-digit scores, but the usual score formating is 2 digits with leading zeros.
        # Adjust the score string to have the same length in both scenarios.
        home_score_str = f" {match.home_score:02d}" if match.home_score < 100 else f"{match.home_score:03d}"
        away_score_str = f"{match.away_score:02d} " if match.away_score < 100 else f"{match.away_score:03d}"

        # Make sure the team name does not overflow the column.
        max_str_length = column_width - self.COLUMN_PADDING
        # The magic "-3" is for the length of ellipsis suffix.
        home_display_name = match.home if len(match.home) < max_str_length else match.home[:max_str_length - 3] + "..."
        away_display_name = match.away if len(match.away) < max_str_length else match.away[:max_str_length - 3] + "..."

        if pretty:
            match_line = self._home_color + f"{home_display_name:<{column_width}}{home_score_str}" + self._color_end
            match_line += ":"
            match_line += self._away_color + f"{away_score_str}{away_display_name:>{column_width}}" + self._color_end
            match_line += "\n"
        else:
            match_line = f"{home_display_name:<{column_width}}{home_score_str}"
            match_line += ":"
            match_line += f"{away_score_str}{away_display_name:>{column_width}}"
            match_line += "\n"

        return match_line

    def _get_column_width(self, matches: List[Match]) -> int:
        """Calculates column width for the home / away halves of the summary string.

        Args:
            matches (List[Match]): List of matches to include in the summary.
            padding (int, optional): Padding added to team names. Defaults to 5.

        Returns:
            int: Column width for the home / away halves of the summary string.
        """
        max_home_name_length = max((len(match.home) for match in matches), default=0)
        max_away_name_length = max((len(match.away) for match in matches), default=0)
        max_name_length = max([max_home_name_length, max_away_name_length, self.MIN_COLUMN_WIDTH])

        return min(max_name_length, self.MAX_COLUMN_WIDTH) + self.COLUMN_PADDING

    def _get_summary_header(self, column_width: int) -> str:
        """Adds a simple header to the summary table.

        Args:
            column_width (int): Column width for the home / away halves of the summary string.

        Returns:
            str: Header string in a "HOME   |   AWAY\n-----------" format.
        """
        home_header = self.HOME_HEADER
        away_header = self.AWAY_HEADER
        header_line = self._home_color + f"{home_header:<{column_width}}   " + self._color_end + "|"
        header_line += self._away_color + f"   {away_header:>{column_width}}" + self._color_end + "\n"
        # The magic "7" is the total width of extra characters (whitespaces and ":") present in each
        # summary line. It's added for consistent width.
        header_line += "-" * (2 * column_width + 7) + "\n"
        return header_line

    def _get_summary_footer(self, column_width: int) -> str:
        """Adds a simplistic footer to the summary table.

        Args:
            column_width (int): Column width for the home / away halves of the summary string.

        Returns:
            str: String containing only "-", spanning the table width.
        """
        # The magic "7" is the total width of extra characters (whitespaces and ":") present in each
        # summary line. It's added for consistent width.
        return "-" * (2 * column_width + 7) + "\n"

    def summary(self, pretty=False, max_lines: int | None = None, start_from: int = 0) -> str:
        """Return the summary string.

        Args:
            pretty (bool, optional): Use slightly improved formatting. Defaults to False.
            max_lines (int, optional): Max lines (max number of matches) to display. Defaults to 20.
            start_from (int, optional): Index in the sorted matches list to start the summary from. Defaults to 0.

        Returns:
            str: String with a summary of ongoing games formatted as: "Uruguay        06:06          Italy".
        """
        summary_string = ""

        if max_lines is None:
            max_lines = self.MAX_SUMMARY_LINES

        # Select matches to include in the summary. Max lines and start_from can be used to implement pagination.
        matches, ellipsis = self._get_matches_for_summary(max_lines, start_from)
        # Column width for both halves (home / away) of the table. Based on the longest team name.
        col_width = self._get_column_width(matches)

        # Make sure the platform is linux, for command line colors.
        is_linux = False
        if platform == "linux" or platform == "linux2":
            is_linux = True

        if pretty and is_linux:
            summary_string += self._get_summary_header(col_width)
        for m in matches:
            if pretty and is_linux:
                summary_string += self._match_printer(m, col_width, pretty=True)
            else:
                summary_string += self._match_printer(m, col_width)

        if ellipsis:
            summary_string += self.TABLE_ELLIPSIS
        if pretty and is_linux:
            summary_string += self._get_summary_footer(col_width)
        return summary_string
