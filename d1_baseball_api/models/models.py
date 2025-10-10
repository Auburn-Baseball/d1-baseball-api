from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict
from datetime import date


class ConferenceTeam(BaseModel):
    TeamName: str
    TrackmanAbbreviation: str


class Team(BaseModel):
    TeamName: str
    TrackmanAbbreviation: str
    Mascot: str
    Conference: str


class SeasonDates(BaseModel):
    year: int
    season_start: date
    season_end: date
