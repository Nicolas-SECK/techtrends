import pandas as pd
from src.stats import top_tags


def test_top_tags_counts():
    df = pd.DataFrame(
        [
            {"tags": "python,ai", "source": "devto"},
            {"tags": "python", "source": "devto"},
            {"tags": "ai", "source": "devto"},
        ]
    )

    out = top_tags(df, n=5)
    # On s'attend à python=2, ai=2 (ordre possible)
    counts = dict(zip(out["tags"], out["count"]))

    assert counts.get("python", 0) == 2
    assert counts.get("ai", 0) == 2
