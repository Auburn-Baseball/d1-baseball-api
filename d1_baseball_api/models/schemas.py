from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict
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
    year: int
    season_start: date
    season_end: date
