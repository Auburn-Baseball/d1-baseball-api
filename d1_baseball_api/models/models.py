from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class ConferenceTeam(BaseModel):
    TeamName: str
    TrackmanAbbreviation: str


class Team(BaseModel):
    TeamName: str
    TrackmanAbbreviation: str
    Mascot: str
    Conference: str
