import sys
import re
from typing import Optional, List, Dict, Tuple, Iterable, Union
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date


def URL(year: int) -> str:
    return (
        "https://en.wikipedia.org/wiki/{year}_NCAA_Division_I_baseball_season".format(
            year=year
        )
    )


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/127.0.0.0 Safari/537.36"
}

MONTHS_RE = r"(January|February|March|April|May|June|July|August|September|October|November|December)"


def norm_text(s: str) -> str:
    return " ".join((s or "").split())


def _parse_month_day_year(text: str, year: str) -> date:
    """Convert 'Month Day' (February 16) into YYYY-MM-DD format YYYY-02-16."""
    text = norm_text(text)
    m = re.match(rf"^{MONTHS_RE} (\d{{1,2}})(, (\d{{4}}))?$", text)

    month_str, day_str, _, year_str = m.groups()
    month = datetime.strptime(month_str, "%B").month
    day = int(day_str)
    year = int(year)

    return date(year, month, day)


def _extract_duration_dates(text: str, year: int) -> Optional[Tuple[date, date]]:
    text = norm_text(text).replace("*", "")
    dates, year = text.split(", ")
    start_month_day, end_month_day = re.split(r"\s*–\s*", dates)

    if not any(m in start_month_day for m in MONTHS_RE) or not any(
        m in end_month_day for m in MONTHS_RE
    ):
        return None

    start_date = _parse_month_day_year(start_month_day, year)
    end_date = _parse_month_day_year(end_month_day, year)

    return start_date, end_date


def _scrape_season_dates(year: int, url: str) -> Tuple[date, date]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(2)

    soup = BeautifulSoup(resp.text, "html.parser")
    infobox = soup.find("table", class_=lambda value: value and "infobox" in value)

    for row in infobox.find_all("tr"):
        header_cell = row.find("th")
        if not header_cell:
            continue
        if header_cell.get_text(" ", strip=True).lower() != "duration":
            continue
        data_cell = row.find("td", class_="infobox-data")
        if not data_cell:
            continue

        range_text = data_cell.get_text(" ", strip=True)
        dates = _extract_duration_dates(range_text, year)
        if dates:
            return dates

    return None, None


def extract_season_dates_for_year(year: int) -> Dict[str, Union[int, date]]:
    season: Dict[str, Union[int, date]] = {}
    url = URL(year)
    season_start, season_end = _scrape_season_dates(year, url)

    if season_start and season_end:
        season["year"] = year
        season["season_start"] = season_start
        season["season_end"] = season_end

    return season
