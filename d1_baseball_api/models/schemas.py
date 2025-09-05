from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class MessageResponse(BaseModel):
    message: str


class ConferencesResponse(RootModel[Dict[str, List[str]]]):
    """Response model for conferences endpoint - Dictionary of conference names to team lists"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "SEC": ["Alabama", "Auburn", "Georgia", "LSU", "Tennessee"],
                "ACC": ["Duke", "North Carolina", "Virginia", "Clemson", "Miami"],
                "Big 12": ["Texas", "Oklahoma", "Kansas", "Baylor", "TCU"],
                "Big Ten": ["Ohio State", "Michigan", "Penn State", "Iowa"],
            }
        }
    }


class TeamConference(BaseModel):
    """Individual team-conference record"""

    TeamName: str
    Conference: str
    Year: int


class TeamsResponse(RootModel[Dict[str, List[str]]]):
    """Response model for teams endpoint - List of D1 teams"""

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "TrackmanAbbreviation": "AUB_TIG",
                    "TeamName": "Auburn Tigers",
                    "Stadium": "Plainsman Park",
                    "Mascot": "Tigers",
                },
                {
                    "TrackmanAbbreviation": "VAN_COM",
                    "TeamName": "Vanderbilt Commodores",
                    "Stadium": "Vanderbilt",
                    "Mascot": "Commodores",
                }
            ]
        }
    }


class TeamConference(BaseModel):
    """Individual team-conference record"""

    TeamName: str
    Conference: str
    Year: int
