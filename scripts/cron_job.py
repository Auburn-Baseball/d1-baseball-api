from d1_conferences_scraper import extract_conferences
from d1_season_dates_scraper import extract_season_dates_for_year
import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client, Client


def update_season_dates(supabase: Client):
    current_year = datetime.now().year
    season = extract_season_dates_for_year(current_year)
    if not season:
        print(f"No season dates found for {current_year}")
        return

    payload = {
        "year": season["year"],
        "season_start": season["season_start"].isoformat(),
        "season_end": season["season_end"].isoformat(),
    }

    try:
        supabase.table("SeasonDates").upsert(payload, on_conflict="year").execute()
        print(f"Upserted season dates for {current_year}")
    except Exception as e:
        print(f"Error upserting season dates: {e}")


def update_teams_and_conferences(supabase: Client):
    current_year = datetime.now().year
    conferences = extract_conferences()

    team_conference_data = []
    for conference_name, teams in conferences.items():
        for team_name in teams:
            team_conference_data.append(
                {
                    "TeamName": team_name,
                    "Conference": conference_name,
                    "Year": current_year,
                }
            )

    try:
        supabase.table("TeamConferences").upsert(
            team_conference_data, on_conflict=["TeamName", "Year"]
        ).execute()
        print(
            f"Successfully upserted {len(team_conference_data)} team-conference records for {current_year}"
        )
    except Exception as e:
        print(f"Error upserting data: {e}")


if __name__ == "__main__":
    # NOTE: Run this script ~YEARLY to update season dates and conferences
    load_dotenv()
    SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
    SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
    supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

    update_season_dates(supabase)
    update_teams_and_conferences(supabase)
