"""
live_cricket.py

Module for fetching live cricket match details from Google results (web scraping fallback).
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List, Union

# PUBLIC_INTERFACE
def fetch_live_cricket_details(query: str = "cricket match") -> Optional[List[Dict[str, Union[str, float, List[str]]]]]:
    """
    Fetches live cricket match details from Google search.

    Args:
        query (str): The search query for Google (default: "cricket match").

    Returns:
        A list of match info dicts containing team names, score, overs, and more,
        or None if no matches found or an error occurs.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/112.0.0.0 Safari/537.36"
        )
    }
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en"
    try:
        resp = requests.get(url, headers=headers, timeout=6)
        resp.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    matches = []

    # Google cricket match cards sometimes use 'imso_mh__ma' or similar classes
    match_cards = soup.select('.imso-mh__ma-sc') or soup.select('.imso-mh__ma') or []
    for card in match_cards:
        # Extract team names
        teams = [el.text.strip() for el in card.select('.imso_mh__first-tn-ed, .imso_mh__tnal-t')]
        # Extract scores
        scores = [el.text.strip() for el in card.select('.imso_mh__scr-it, .imso_mh__scr')]
        # Extract overs and status
        overs = None
        status = None
        status_els = card.select('.imso_mh__lv-m-stts, .imso_mh__lv-m-stts-cont')
        if status_els:
            status = status_els[0].text.strip()

        overs_els = card.select('.imso_mh__lv-m-ov-txt')
        if overs_els:
            overs = overs_els[0].text.strip()

        match = {
            "team_a": teams[0] if len(teams) > 0 else "",
            "team_b": teams[1] if len(teams) > 1 else "",
            "score_a": scores[0] if len(scores) > 0 else "",
            "score_b": scores[1] if len(scores) > 1 else "",
            "overs": overs or "",
            "status": status or ""
        }
        matches.append(match)

    # As a fallback, try Google's cricket widget main selectors, if above fails
    if not matches:
        widget = soup.select_one('[data-attrid="kc:/sport/cricket:current match"]')
        if widget:
            try:
                team_names = widget.select('.ellipsisize')
                scores = widget.select('.sdvaw')
                if len(team_names) >= 2 and len(scores) >= 2:
                    match = {
                        "team_a": team_names[0].text.strip(),
                        "team_b": team_names[1].text.strip(),
                        "score_a": scores[0].text.strip(),
                        "score_b": scores[1].text.strip(),
                        "overs": "",
                        "status": "",
                    }
                    matches.append(match)
            except Exception:
                pass

    return matches if matches else None
