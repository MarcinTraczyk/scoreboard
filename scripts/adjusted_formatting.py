from scoreboard.scoreboard import Scoreboard

Scoreboard.MAX_SUMMARY_LINES = 3
Scoreboard.COLUMN_PADDING = 5
Scoreboard.MIN_COLUMN_WIDTH = 20
Scoreboard.MAX_COLUMN_WIDTH = 20
Scoreboard.HOME_HEADER = "**HOME**"
Scoreboard.AWAY_HEADER = "**AWAY**"
Scoreboard.TABLE_ELLIPSIS = 26*" " + "(...)\n"

sample_scoreboard = Scoreboard()

sample_scoreboard.start_match("Mexico" + "".join(['A']*200), "Canada")
sample_scoreboard.start_match("Spain", "Brazil")
sample_scoreboard.start_match("Germany", "France")
sample_scoreboard.start_match("Uruguay", "Italy")
sample_scoreboard.start_match("Argentina", "Australia")


sample_scoreboard.update_match_score("Mexico" + "".join(['A']*200), "Canada", 0, 5)
sample_scoreboard.update_match_score("Spain", "Brazil", 10, 2)
sample_scoreboard.update_match_score("Germany", "France", 2, 2)
sample_scoreboard.update_match_score("Uruguay", "Italy", 6, 6)
sample_scoreboard.update_match_score("Argentina", "Australia", 3, 1)

print(sample_scoreboard.summary(pretty=True))
