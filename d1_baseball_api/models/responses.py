from pydantic import BaseModel, RootModel
from typing import List, Dict
from d1_baseball_api.models.models import ConferenceTeam, Team, SeasonDates


class MessageResponse(BaseModel):
    message: str


class ConferencesResponse(RootModel[Dict[str, List[ConferenceTeam]]]):
    """Response model for conferences endpoint - Dictionary of conference names to team lists"""

    model_config = {
        "json_schema_extra": {
            "example": {
                "SEC": [
                    {"TeamName": "Alabama", "TrackmanAbbreviation": "ALA_CRI"},
                    {"TeamName": "Auburn", "TrackmanAbbreviation": "AUB_TIG"},
                ],
                "Big Ten": [
                    {"TeamName": "Ohio State", "TrackmanAbbreviation": "OSU_BUC"},
                    {"TeamName": "Michigan", "TrackmanAbbreviation": "MIC_WOL"},
                ],
            }
        }
    }


class TeamsResponse(RootModel[List[Team]]):
    """Response model for teams endpoint - List of teams"""

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "TrackmanAbbreviation": "AUB_TIG",
                    "TeamName": "Auburn",
                    "Mascot": "Tigers",
                    "Conference": "SEC",
                },
                {
                    "TrackmanAbbreviation": "ALA_CRI",
                    "TeamName": "Alabama",
                    "Mascot": "Crimson Tide",
                    "Conference": "SEC",
                },
            ]
        }
    }


class SeasonDatesResponse(RootModel[List[SeasonDates]]):
    """Response model for season dates endpoint - List of season windows"""

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "year": 2026,
                    "season_start": "2026-02-16",
                    "season_end": "2026-06-30",
                }
            ]
        }
    }
