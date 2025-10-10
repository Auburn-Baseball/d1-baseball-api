import sys
import re
from typing import Optional, List, Dict
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date

URL = "https://www.ncaa.com/championships/baseball/d1/future-info/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/127.0.0.0 Safari/537.36"
}


def norm_text(s: str) -> str:
    return " ".join((s or "").split())


MONTHS_RE = r"(January|February|March|April|May|June|July|August|September|October|November|December)"


def _parse_month_day_year(text: str, fallback_year: str) -> Optional[date]:
    """Extract 'Month Day[, Year]' from text like 'Sun., June 22 (if necessary)'."""
    if not text:
        return None
    text = norm_text(text).replace("*", "")
    m = re.search(rf"{MONTHS_RE}\s+\d{{1,2}}(?:,\s*\d{{4}})?", text)
    if not m:
        return None
    core = m.group(0)
    if "," not in core:
        core = f"{core}, {fallback_year}"
    try:
        return datetime.strptime(core, "%B %d, %Y").date()
    except ValueError:
        return None


def extract_dates() -> List[Dict[str, date]]:
    """
    Return season windows keyed by championship year Y:
      season_end[Y]   = last day of Y's CWS finals
      season_start[Y] = (last day of (Y-1)'s CWS) + 1 day
    """
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {URL}: {e}", file=sys.stderr)
        sys.exit(2)

    soup = BeautifulSoup(resp.text, "html.parser")
    tbody = soup.find("tbody")
    if not tbody:
        print("Could not find <tbody> on Future Dates & Sites page.", file=sys.stderr)
        sys.exit(2)

    # 1) Collect WS end dates per year from the Finals column
    ws_end_by_year: Dict[int, date] = {}
    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue
        year_txt = tds[0].get_text(strip=True)
        if not year_txt.isdigit():
            continue
        y = int(year_txt)

        finals_td = tds[3]
        bits = [
            norm_text(d.get_text(" ", strip=True)) for d in finals_td.find_all("div")
        ]
        if not bits:
            bits = [norm_text(finals_td.get_text(" ", strip=True))]

        candidates = [_parse_month_day_year(b, year_txt) for b in bits]
        finals_dates = [d for d in candidates if d]
        if finals_dates:
            ws_end_by_year[y] = max(finals_dates)  # Sunday or Monday-if-necessary

    # 2) Build season windows using previous year's WS end
    seasons: List[Dict[str, date]] = []
    for y in sorted(ws_end_by_year.keys()):
        prev = y - 1
        if prev not in ws_end_by_year:
            # No prior WS end known → skip, or set season_start=None if you prefer to include it
            continue
        season_start = ws_end_by_year[prev] + timedelta(days=1)
        season_end = ws_end_by_year[y]
        seasons.append(
            {
                "year": y,
                "season_start": season_start,
                "season_end": season_end,
            }
        )
    # print (seasons)
    return seasons


extract_dates()
