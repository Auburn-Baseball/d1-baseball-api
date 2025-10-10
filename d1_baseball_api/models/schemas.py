from pydantic import BaseModel
from datetime import date


class TeamConferenceTable(BaseModel):
    """Individual team-conference record"""

    id: int
    TeamName: str
    Conference: str
    Year: int


class TrackmanTeamMappingTable(BaseModel):
    """Individual trackman-team-mapping record"""

    id: int
    TeamName: str
    TrackmanAbbreviation: str
    Mascot: str


class SeasonDates(BaseModel):
    """Individual season dates record"""

    year: int
    season_start: date
    season_end: date
