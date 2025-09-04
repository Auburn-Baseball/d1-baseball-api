from d1_conferences_scraper import extract_conferences
import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client, Client

if __name__ == "__main__":
    load_dotenv()
    SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
    SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
    supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

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
        result = (
            supabase.table("TeamConferences").insert(team_conference_data).execute()
        )
        print(
            f"Successfully inserted {len(team_conference_data)} team-conference records for {current_year}"
        )
    except Exception as e:
        print(f"Error inserting data: {e}")
