import pandas as pd
from src.normalize import normalize_hn_items, normalize_devto_articles


def test_normalize_hn_items_basic():
    hn_items = [
        {
            "title": "Test HN",
            "url": "https://example.com",
            "by": "alice",
            "score": 123,
            "descendants": 45,
            "time": 1700000000,  # epoch seconds
        }
    ]

    rows = normalize_hn_items(hn_items)
    assert len(rows) == 1

    r = rows[0]
    assert r["source"] == "hackernews"
    assert r["title"] == "Test HN"
    assert r["url"].startswith("http")
    assert r["author"] == "alice"
    assert isinstance(r["score"], int)
    assert isinstance(r["comments"], int)
    assert "published_at" in r  # peut être None ou datetime string selon ton normalize


def test_normalize_devto_articles_basic():
    dev_articles = [
        {
            "title": "Test Dev.to",
            "url": "https://dev.to/test",
            "user": {"name": "Bob"},
            "public_reactions_count": 10,
            "comments_count": 3,
            "tag_list": ["python", "ai"],
            "published_at": "2026-01-01T10:00:00Z",
        }
    ]

    rows = normalize_devto_articles(dev_articles)
    assert len(rows) == 1

    r = rows[0]
    assert r["source"] == "devto"
    assert r["title"] == "Test Dev.to"
    assert r["author"] == "Bob"
    assert r["score"] == 10
    assert r["comments"] == 3
    # tags peut être "python,ai" ou "python ai" selon ton normalize
    assert "python" in str(r["tags"])
    assert "ai" in str(r["tags"])
    assert "published_at" in r
