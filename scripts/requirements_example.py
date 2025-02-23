from scoreboard.scoreboard import Scoreboard


sample_scoreboard = Scoreboard()

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

print(sample_scoreboard.summary(pretty=True))
