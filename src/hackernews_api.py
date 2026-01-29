from __future__ import annotations

from typing import Any, Dict, List
import requests

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"


def _get_json(url: str, timeout: int = 15) -> Any:
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_topstories(limit: int = 20) -> List[Dict[str, Any]]:
    ids = _get_json(f"{HN_BASE_URL}/topstories.json")
    items: List[Dict[str, Any]] = []
    for story_id in ids[:limit]:
        item = _get_json(f"{HN_BASE_URL}/item/{story_id}.json")
        if isinstance(item, dict):
            items.append(item)
    return items
