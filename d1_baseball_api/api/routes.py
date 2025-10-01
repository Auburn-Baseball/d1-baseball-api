from fastapi import APIRouter, HTTPException
from d1_baseball_api.database import get_supabase
from d1_baseball_api.models.responses import (
    MessageResponse,
    ConferencesResponse,
    ConferenceResponse,
    TeamsResponse,
    TeamResponse,
)
from typing import Dict, List
from d1_baseball_api.models.models import ConferenceTeam, Team, SeasonDates
import os
from supabase import create_client

router = APIRouter()

def _sb():
    url = os.getenv("SUPABASE_PROJECT_URL")
    key = os.getenv("SUPABASE_API_KEY")
    return create_client(url, key)

@router.get("/", response_model=MessageResponse)
async def read_root():
    return {"message": "D1 Baseball API built by Auburn University!"}


@router.get("/conferences", response_model=ConferencesResponse)
async def get_conferences_by_year(year: int) -> Dict[str, List[ConferenceTeam]]:
    """
    Get all conferences and their teams for a specific year.

    - **year**: The year to get conference data for (e.g., 2025)

    Returns a dictionary where keys are conference names and values are lists of teams.
    """
    try:
        supabase = get_supabase()
        response = (
            supabase.table("TeamConferences")
            .select("TeamName, Conference, TrackmanTeamMappings(TrackmanAbbreviation)")
            .eq("Year", year)
            .execute()
        )

        if not response.data:
            return {}

        conferences = {}
        for record in response.data:
            conference_name = record["Conference"]
            team_name = record["TeamName"]
            trackman_abbrev = record["TrackmanTeamMappings"]["TrackmanAbbreviation"]

            if conference_name not in conferences:
                conferences[conference_name] = []

            team_data = {
                "TeamName": team_name,
                "TrackmanAbbreviation": trackman_abbrev,
            }
            conferences[conference_name].append(team_data)

        for conference in conferences:
            conferences[conference].sort(key=lambda x: x["TeamName"])

        return conferences

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@router.get("/conference", response_model=ConferenceResponse)
async def get_conference_by_year(year: int, conference: str) -> List[ConferenceTeam]:
    """
    Get all teams within a conference for a specific year.

    - **year**: The year to get conference data for (e.g., 2025)
    - **conference**: The conference to get conference data for (e.g., SEC)

    Returns a list of conference teams.
    """
    try:
        supabase = get_supabase()
        response = (
            supabase.table("TeamConferences")
            .select("TeamName, Conference, TrackmanTeamMappings(TrackmanAbbreviation)")
            .eq("Year", year)
            .eq("Conference", conference)
            .execute()
        )

        if not response.data:
            return {}

        conference_teams = []
        for record in response.data:
            conference_name = record["Conference"]
            team_name = record["TeamName"]
            trackman_abbrev = record["TrackmanTeamMappings"]["TrackmanAbbreviation"]

            team_data = {
                "TeamName": team_name,
                "TrackmanAbbreviation": trackman_abbrev,
            }
            conference_teams.append(team_data)

        conference_teams.sort(key=lambda x: x["TeamName"])

        return conference_teams

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@router.get("/teams", response_model=TeamsResponse)
async def get_teams_by_year(year: int) -> Dict[str, List[Team]]:
    """
    Get all teams for a specific year.

    - **year**: The year to get team data for (e.g., 2025)

    Returns a list of teams for a specific year.
    """
    try:
        supabase = get_supabase()
        response = (
            supabase.table("TeamConferences")
            .select(
                "TeamName, Conference, TrackmanTeamMappings!inner(TrackmanAbbreviation, Mascot)"
            )
            .eq("Year", year)
            .execute()
        )

        if not response.data:
            return {}

        teams = []
        for record in response.data:
            conference_name = record["Conference"]
            team_name = record["TeamName"]
            trackman_abbrev = record["TrackmanTeamMappings"]["TrackmanAbbreviation"]
            mascot = record["TrackmanTeamMappings"]["Mascot"]

            team_data = {
                "TeamName": team_name,
                "TrackmanAbbreviation": trackman_abbrev,
                "Mascot": mascot,
                "Conference": conference_name,
            }
            teams.append(team_data)

        teams.sort(key=lambda x: (x["Conference"], x["TeamName"]))

        return teams

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@router.get("/team", response_model=TeamResponse)
async def get_team_by_year_and_trackman(year: int, trackman: str) -> Dict[str, Team]:
    """
    Get team for a specific year and trackman abbreviation.

    - **year**: The year to get team data for (e.g., 2025)
    - **trackman**: The trackman abbreviation to get team data for (e.g., AUB_TIG)

    Returns a team for a specific year.
    """
    try:
        supabase = get_supabase()
        response = (
            supabase.table("TeamConferences")
            .select(
                "TeamName, Conference, TrackmanTeamMappings!inner(TrackmanAbbreviation, Mascot)"
            )
            .eq("Year", year)
            .eq("TrackmanTeamMappings.TrackmanAbbreviation", trackman)
            .execute()
        )

        if not response.data:
            return {}

        record = response.data[0]
        conference_name = record["Conference"]
        team_name = record["TeamName"]
        trackman_abbrev = record["TrackmanTeamMappings"]["TrackmanAbbreviation"]
        mascot = record["TrackmanTeamMappings"]["Mascot"]

        team_data = {
            "TeamName": team_name,
            "TrackmanAbbreviation": trackman_abbrev,
            "Mascot": mascot,
            "Conference": conference_name,
        }

        return team_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    
@router.get("/season-dates/{year}", response_model=SeasonDates)
async def get_season_dates(year: int):
    """
    Return the JSON season window for a given year from the SeasonDates table.
    200: {"year": 2027, "season_start": "2026-06-23", "season_end": "2027-06-28"}
    404: {"detail": "Season dates for 2025 not found"}
    """
    sb = _sb()
    resp = sb.table("SeasonDates").select("*").eq("year", year).single().execute()
    row = resp.data
    if not row:
        raise HTTPException(status_code=404, detail=f"Season dates for {year} not found")
    # FastAPI + Pydantic will serialize to JSON automatically
    return SeasonDates(**row)



