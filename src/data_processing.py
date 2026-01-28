"""
Module de traitement et analyse des données
"""
import pandas as pd
from typing import List, Dict, Tuple, Any
import logging
from datetime import datetime, timedelta
import re
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Classe pour traiter et analyser les données d'articles"""

    def __init__(self):
        self.stop_words = set([
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "should", "could", "may", "might", "can", "this", "that",
            "these", "those", "i", "you", "he", "she", "it", "we", "they"
        ])

    def articles_to_dataframe(self, articles: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convertit une liste d'articles en DataFrame"""
        if not articles:
            logger.warning("No articles to convert")
            return pd.DataFrame()

        df = pd.DataFrame(articles)

        # Titre
        if "title" in df.columns:
            df["title"] = df["title"].fillna("").astype(str)

        # Dates
        for col in ["published_at", "scraped_at", "fetched_at"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Numériques
        numeric_cols = ["points", "comments", "reactions", "reading_time"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        logger.info(f"Created DataFrame with {len(df)} articles and {len(df.columns)} columns")
        return df

    def merge_sources(self, *dfs: pd.DataFrame) -> pd.DataFrame:
        """Fusionne plusieurs DataFrames (supprime doublons sur le titre)"""
        valid = [d for d in dfs if not d.empty]
        if not valid:
            return pd.DataFrame()

        merged = pd.concat(valid, ignore_index=True)

        if "title" in merged.columns:
            merged = merged.drop_duplicates(subset=["title"], keep="first")

        logger.info(f"Merged {len(valid)} sources into {len(merged)} articles")
        return merged

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Extrait les mots-clés les plus fréquents d'un texte"""
        if not text:
            return []

        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        words = text.split()

        filtered = [w for w in words if w not in self.stop_words and len(w) > 3]
        counts = Counter(filtered)
        return counts.most_common(top_n)

    def categorize_by_keywords(self, df: pd.DataFrame, keywords_dict: Dict[str, List[str]]) -> pd.DataFrame:
        """Catégorise les articles selon des mots-clés dans le titre"""
        if df.empty or "title" not in df.columns:
            return df

        def find_cat(title: str) -> str:
            t = title.lower()
            scores = {}
            for cat, kws in keywords_dict.items():
                score = sum(1 for k in kws if k.lower() in t)
                if score > 0:
                    scores[cat] = score
            return max(scores, key=scores.get) if scores else "Other"

        df["category"] = df["title"].apply(find_cat)
        logger.info(f"Categories: {df['category'].value_counts().to_dict()}")
        return df

    def get_trending_topics(self, df: pd.DataFrame, column: str = "title", top_n: int = 20) -> List[Tuple[str, int]]:
        """Identifie les sujets tendances à partir d'une colonne texte"""
        if df.empty or column not in df.columns:
            return []

        text = " ".join(df[column].dropna().astype(str))
        return self.extract_keywords(text, top_n=top_n)

    def get_top_articles(self, df: pd.DataFrame, metric: str = "points", top_n: int = 10) -> pd.DataFrame:
        """Top articles selon une métrique"""
        if df.empty or metric not in df.columns:
            return pd.DataFrame()
        return df.nlargest(top_n, metric)

    def get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Statistiques générales sur les articles"""
        if df.empty:
            return {}

        stats: Dict[str, Any] = {
            "total_articles": len(df),
            "sources": df["source"].value_counts().to_dict() if "source" in df.columns else {},
        }

        if "points" in df.columns:
            stats["avg_points"] = float(df["points"].mean())
            stats["median_points"] = float(df["points"].median())
            stats["max_points"] = int(df["points"].max())

        if "reactions" in df.columns:
            stats["avg_reactions"] = float(df["reactions"].mean())
            stats["total_reactions"] = int(df["reactions"].sum())

        if "comments" in df.columns:
            stats["avg_comments"] = float(df["comments"].mean())
            stats["total_comments"] = int(df["comments"].sum())

        if "category" in df.columns:
            stats["categories"] = df["category"].value_counts().to_dict()

        return stats


if __name__ == "__main__":
    sample_articles = [
        {"title": "Introduction to Python Machine Learning", "points": 150, "source": "HackerNews"},
        {"title": "Docker Tutorial for Beginners", "points": 95, "source": "Dev.to"},
        {"title": "JavaScript Framework Comparison", "points": 200, "source": "HackerNews"},
    ]

    p = DataProcessor()
    df = p.articles_to_dataframe(sample_articles)
    print("\n✅ DF:")
    print(df)

    kws = {
        "Python": ["python", "machine learning"],
        "DevOps": ["docker", "kubernetes"],
        "JavaScript": ["javascript", "framework"],
    }
    df = p.categorize_by_keywords(df, kws)
    print("\n📊 Categories:")
    print(df[["title", "category"]])
