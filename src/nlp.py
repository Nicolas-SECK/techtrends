from __future__ import annotations

import re
from typing import List
import pandas as pd

# Stopwords minimalistes (on évite NLTK download dans Docker)
STOPWORDS_EN = {
    "the","a","an","and","or","to","of","in","on","for","with","from","is","are","was","were",
    "as","at","by","be","this","that","it","its","into","over","how","why","what","when","where",
    "your","you","we","our","they","their","i","me","my"
}
STOPWORDS_FR = {
    "le","la","les","un","une","des","et","ou","de","du","dans","sur","pour","avec","par","au","aux",
    "est","sont","été","être","ce","cet","cette","ces","il","elle","ils","elles","nous","vous","mon","ma","mes",
    "son","sa","ses","leur","leurs","que","qui","quoi","quand","où","comment","pourquoi"
}

STOPWORDS = STOPWORDS_EN | STOPWORDS_FR


def tokenize_titles(df: pd.DataFrame) -> List[str]:
    titles = df.get("title", pd.Series([], dtype=str)).fillna("").astype(str)
    text = " ".join(titles.tolist()).lower()
    # keep letters/numbers, split on non-word
    tokens = re.findall(r"[a-z0-9]+", text)
    tokens = [t for t in tokens if len(t) >= 3 and t not in STOPWORDS]
    return tokens


def top_words(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    tokens = tokenize_titles(df)
    if not tokens:
        return pd.DataFrame(columns=["word", "count"])
    s = pd.Series(tokens).value_counts().head(n).reset_index()
    s.columns = ["word", "count"]
    return s
