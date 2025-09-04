from fastapi import APIRouter, HTTPException
from d1_baseball_api.database import get_supabase
from d1_baseball_api.models.schemas import MessageResponse, ConferencesResponse
from typing import Dict, List

router = APIRouter()


@router.get("/", response_model=MessageResponse)
async def read_root():
    return {"message": "D1 Baseball API built by Auburn University!"}


@router.get("/conferences/{year}", response_model=ConferencesResponse)
async def get_conferences_by_year(year: int) -> Dict[str, List[str]]:
    """
    Get all conferences and their teams for a specific year.

    - **year**: The year to get conference data for (e.g., 2025)

    Returns a dictionary where keys are conference names and values are lists of team names.
    """
    try:
        supabase = get_supabase()
        response = (
            supabase.table("TeamConferences")
            .select("TeamName, Conference")
            .eq("Year", year)
            .execute()
        )

        if not response.data:
            return {}

        conferences = {}
        for record in response.data:
            conference_name = record["Conference"]
            team_name = record["TeamName"]

            if conference_name not in conferences:
                conferences[conference_name] = []

            conferences[conference_name].append(team_name)

        for conference in conferences:
            conferences[conference].sort()

        return conferences

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
