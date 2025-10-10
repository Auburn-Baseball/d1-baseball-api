from fastapi import APIRouter, HTTPException
from d1_baseball_api.database import get_supabase
from d1_baseball_api.models.responses import (
    MessageResponse,
    ConferencesResponse,
    TeamsResponse,
    SeasonDatesResponse,
)
from typing import Dict, List
from d1_baseball_api.models.models import ConferenceTeam, Team, SeasonDates

router = APIRouter()


@router.get("/", response_model=MessageResponse)
async def read_root():
    return {"message": "D1 Baseball API built by Auburn University!"}


@router.get("/conferences", response_model=ConferencesResponse)
async def get_conferences(
    year: int, conference: str | None = None
) -> Dict[str, List[ConferenceTeam]]:
    """
    Get conferences and their teams for a specific year.

    - **year**: The season year to query (e.g., 2025)
    - **conference**: Optional conference filter (e.g., SEC). When provided the response contains only that conference.
    """
    requested_conference = conference
    try:
        supabase = get_supabase()
        query = (
            supabase.table("TeamConferences")
            .select("TeamName, Conference, TrackmanTeamMappings(TrackmanAbbreviation)")
            .eq("Year", year)
        )
        if requested_conference:
            query = query.eq("Conference", requested_conference)

        response = query.execute()

        if not response.data:
            detail = (
                f"No conference data found for year {year}"
                if not requested_conference
                else f"No conference data found for year {year} and conference {requested_conference}"
            )
            raise HTTPException(status_code=404, detail=detail)

        conferences: Dict[str, List[Dict[str, str]]] = {}
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

        for conference_name in conferences:
            conferences[conference_name].sort(key=lambda x: x["TeamName"])

        if requested_conference and requested_conference in conferences:
            return {requested_conference: conferences[requested_conference]}

        return conferences

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@router.get("/teams", response_model=TeamsResponse)
async def get_teams(
    year: int, conference: str | None = None, trackman: str | None = None
) -> List[Team]:
    """
    Get teams for a specific year.

    - **year**: The season year to query (e.g., 2025)
    - **conference**: Optional conference filter.
    - **trackman**: Optional TrackMan abbreviation filter. When provided the list contains at most one team.
    """
    try:
        supabase = get_supabase()
        query = (
            supabase.table("TeamConferences")
            .select(
                "TeamName, Conference, TrackmanTeamMappings!inner(TrackmanAbbreviation, Mascot)"
            )
            .eq("Year", year)
        )
        if conference:
            query = query.eq("Conference", conference)
        if trackman:
            query = query.eq("TrackmanTeamMappings.TrackmanAbbreviation", trackman)

        response = query.execute()

        if not response.data:
            filters = []
            filters.append(f"year {year}")
            if conference:
                filters.append(f"conference {conference}")
            if trackman:
                filters.append(f"TrackMan {trackman}")
            detail = f"No team data found for {' and '.join(filters)}"
            raise HTTPException(status_code=404, detail=detail)

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


@router.get("/season-dates", response_model=SeasonDatesResponse)
async def get_season_dates(year: int | None = None) -> List[SeasonDates]:
    """
    Get the season window for a specific year.

    - **year**: The year to retrieve season dates for (e.g., 2026)

    Returns a list containing the season window for the requested year.
    """
    try:
        supabase = get_supabase()
        query = supabase.table("SeasonDates").select("year, season_start, season_end")
        if year is not None:
            query = query.eq("year", year)

        response = query.execute()

        if year is not None and not response.data:
            raise HTTPException(
                status_code=404, detail=f"Season dates for {year} not found"
            )

        season_dates = [SeasonDates(**record) for record in response.data]
        return season_dates

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
