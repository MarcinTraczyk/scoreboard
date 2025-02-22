from pydantic import BaseModel, conint, ConfigDict, model_validator


MAX_TEAM_GOALS = 1000


class Match(BaseModel):
    home: str
    away: str
    home_score: conint(ge=0, lt=MAX_TEAM_GOALS) = 0
    away_score: conint(ge=0, lt=MAX_TEAM_GOALS) = 0

    # Modify the pydantic config, so the validations are run on field assignments.
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode='after')
    def capitalize(self) -> str:
        """Ensure the home and away team names are different. Case insensitive. """
        if self.home.lower() == self.away.lower():
            raise ValueError("Home and away teams must be different.")
        return self

    @property
    def total_score(self) -> int:
        return self.home_score + self.away_score
