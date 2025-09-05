from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


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
