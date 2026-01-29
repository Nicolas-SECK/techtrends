from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _ts_to_dt(ts: Optional[int]) -> Optional[datetime]:
    """Unix timestamp (seconds) -> datetime UTC."""
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _iso_to_dt(s: Optional[str]) -> Optional[datetime]:
    """ISO string -> datetime (timezone-aware if possible)."""
    if not s:
        return None
    try:
        # Dev.to often returns ISO like: 2026-01-29T14:51:56Z or with offset
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_hn_items(hn_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for it in hn_items:
        rows.append(
            {
                "source": "hackernews",
                "title": it.get("title"),
                "author": it.get("by"),
                "score": it.get("score"),
                "comments": it.get("descendants"),
                "tags": "",
                "url": it.get("url") or f"https://news.ycombinator.com/item?id={it.get('id')}",
                "published_at": _ts_to_dt(it.get("time")),
            }
        )
    return rows


def normalize_devto_articles(dev_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for a in dev_articles:
        rows.append(
            {
                "source": "devto",
                "title": a.get("title"),
                "author": (a.get("user") or {}).get("name"),
                "score": a.get("public_reactions_count"),
                "comments": a.get("comments_count"),
                "tags": ",".join(a.get("tag_list") or []),
                "url": a.get("url"),
                "published_at": _iso_to_dt(a.get("published_at")),
            }
        )
    return rows
