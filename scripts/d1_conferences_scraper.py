import json
import sys
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


URL = "https://d1baseball.com/conferences/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/127.0.0.0 Safari/537.36"
}


def norm_text(s: str) -> str:
    return " ".join((s or "").split())


def extract_conferences() -> Dict[str, List[str]]:
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {URL}: {e}", file=sys.stderr)
        sys.exit(2)

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    conf_map: Dict[str, List[str]] = {}

    for conf_div in soup.select("div.conference-list"):
        h3 = conf_div.find("h3")
        if not h3:
            print("Warning: conference div missing h3", file=sys.stderr)
            continue
        conf_name = norm_text(h3.get_text(" ", strip=True))
        if not conf_name:
            print("Warning: conference with empty name", file=sys.stderr)
            continue

        teams: List[str] = []
        tbody = conf_div.select_one("table tbody")
        if tbody:
            for row in tbody.select("tr"):
                link = None
                if "team" in (row.get("class") or []):
                    link = row.select_one("a")
                if not link:
                    link = row.select_one("td.team a")
                if not link:
                    link = row.find("a")
                if not link:
                    print(
                        f"Warning: conference {conf_name} has row with no link",
                        file=sys.stderr,
                    )
                    continue

                team_name = norm_text(link.get_text(" ", strip=True))
                if team_name:
                    teams.append(team_name)
                else:
                    print(
                        f"Warning: conference {conf_name} has row with empty team name",
                        file=sys.stderr,
                    )

        conf_map[conf_name] = teams

    return conf_map
