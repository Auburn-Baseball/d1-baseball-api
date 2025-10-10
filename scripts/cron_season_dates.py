# scripts/cron_season_dates.py
from season_start_end_dates import extract_dates
import os, sys
from dotenv import load_dotenv
from supabase import create_client
from datetime import date

load_dotenv()
url = os.getenv("SUPABASE_PROJECT_URL")
key = os.getenv("SUPABASE_API_KEY")
if not url or not key:
    print("Missing SUPABASE_PROJECT_URL or SUPABASE_API_KEY", file=sys.stderr)
    sys.exit(1)

supabase = create_client(url, key)

def ensure_year_exists(year: int, season_start: date, season_end: date):
    """Insert a year row if it's not already in SeasonDates."""
    resp = supabase.table("SeasonDates").select("year").eq("year", year).execute()
    if resp.data:
        print(f"Year {year} already exists. Skipping insert.")
        return
    supabase.table("SeasonDates").insert({
        "year": year,
        "season_start": season_start,
        "season_end": season_end,
    }).execute()
    print(f"Inserted {year}: {season_start} → {season_end}")

if __name__ == "__main__":
    try:
        seasons = extract_dates()
        for s in seasons:
            ensure_year_exists(
                int(s["year"]),
                s["season_start"],
                s["season_end"],
            )
    except Exception as e:
        print(f"Error updating season dates: {e}", file=sys.stderr)
        sys.exit(1)
