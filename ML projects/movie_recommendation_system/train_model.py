"""Train a weighted content-based movie recommender from the TMDB 5000 CSV files."""
from pathlib import Path
import ast
import pickle
import re
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTIFACT_DIR = BASE_DIR / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)
DATA_DIR = Path(r"D:\movie_recommender_improved\data")

MOVIES_CSV = DATA_DIR / "tmdb_5000_movies.csv"
CREDITS_CSV = DATA_DIR / "tmdb_5000_credits.csv"

# Feature weights: metadata is deliberately emphasized over cast/director names.
WEIGHTS = {
    "overview": 1.0,
    "genres": 2.0,
    "keywords": 1.8,
    "cast": 1.0,
    "director": 1.2,
}
MAX_FEATURES = 12000
stemmer = PorterStemmer()


def parse_json_names(value, limit=None):
    """Parse TMDB JSON-like columns safely and return their name values."""
    if pd.isna(value):
        return []
    try:
        parsed = ast.literal_eval(value) if isinstance(value, str) else value
    except (ValueError, SyntaxError):
        return []
    if not isinstance(parsed, list):
        return []
    names = []
    for item in parsed:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]))
        if limit is not None and len(names) >= limit:
            break
    return names


def get_director(value):
    if pd.isna(value):
        return []
    try:
        crew = ast.literal_eval(value) if isinstance(value, str) else value
    except (ValueError, SyntaxError):
        return []
    if isinstance(crew, list):
        for person in crew:
            if isinstance(person, dict) and person.get("job") == "Director":
                return [str(person.get("name", ""))]
    return []


def clean_tokens(items):
    """Normalize phrases, remove duplicates while preserving first occurrence."""
    output, seen = [], set()
    for item in items:
        phrase = re.sub(r"[^a-zA-Z0-9 ]+", " ", str(item).lower())
        phrase = re.sub(r"\s+", " ", phrase).strip()
        if not phrase:
            continue
        # Keep multiword names together as one token for metadata fields.
        token = phrase.replace(" ", "")
        if token not in seen:
            output.append(token)
            seen.add(token)
    return output


def clean_overview(value):
    if pd.isna(value):
        return ""
    words = re.findall(r"[a-zA-Z0-9]+", str(value).lower())
    # Stem each word, then remove repeated stems without changing order.
    seen, result = set(), []
    for word in words:
        stemmed = stemmer.stem(word)
        if stemmed not in seen:
            seen.add(stemmed)
            result.append(stemmed)
    return " ".join(result)


def clean_metadata(items):
    tokens = clean_tokens(items)
    # Stem metadata phrases too, but keep each phrase as a single token.
    return " ".join(stemmer.stem(token) for token in tokens)


def main():
    if not MOVIES_CSV.exists() or not CREDITS_CSV.exists():
        raise FileNotFoundError(
            "CSV files not found. Put tmdb_5000_movies.csv and "
            "tmdb_5000_credits.csv inside the project's data/ folder."
        )

    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV)
    # The TMDB credits file has its own id column; movie_id comes from movies.
    credits = credits.drop(columns=["title"], errors="ignore")
    if "movie_id" not in movies.columns:
        movies = movies.rename(columns={"id": "movie_id"})
    if "movie_id" not in credits.columns and "id" in credits.columns:
        credits = credits.rename(columns={"id": "movie_id"})

    df = movies.merge(credits, on="movie_id", how="inner", suffixes=("", "_credits"))
    required = ["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns after merge: {missing}")

    df = df[required].copy()
    df = df.dropna(subset=["title"]).drop_duplicates(subset=["movie_id"]).reset_index(drop=True)
    df["overview_display"] = df["overview"].fillna("").astype(str)

    df["overview_text"] = df["overview"].apply(clean_overview)
    df["genres_list"] = df["genres"].apply(parse_json_names)
    df["keywords_list"] = df["keywords"].apply(parse_json_names)
    df["cast_list"] = df["cast"].apply(lambda x: parse_json_names(x, limit=3))
    df["director_list"] = df["crew"].apply(get_director)

    df["genres_text"] = df["genres_list"].apply(clean_metadata)
    df["keywords_text"] = df["keywords_list"].apply(clean_metadata)
    df["cast_text"] = df["cast_list"].apply(clean_metadata)
    df["director_text"] = df["director_list"].apply(clean_metadata)

    # Separate vectorizers make feature weighting explicit and easy to tune.
    matrices = []
    vectorizer_info = {}
    for field, weight in WEIGHTS.items():
        vectorizer = CountVectorizer(
            max_features=MAX_FEATURES,
            stop_words="english",
            binary=True
        )
        matrix = vectorizer.fit_transform(df[f"{field}_text"])
        matrices.append(matrix * weight)
        vectorizer_info[field] = vectorizer

    combined = hstack(matrices).tocsr()
    similarity = cosine_similarity(combined, dense_output=True)

    # Keep only app-facing fields in the metadata artifact.
    catalog = df[[
        "movie_id", "title", "overview_display",
        "genres_list", "keywords_list", "cast_list", "director_list"
    ]].copy()

    with open(ARTIFACT_DIR / "movie_catalog.pkl", "wb") as f:
        pickle.dump(catalog, f)
    with open(ARTIFACT_DIR / "similarity.pkl", "wb") as f:
        pickle.dump(similarity, f)
    with open(ARTIFACT_DIR / "feature_config.pkl", "wb") as f:
        pickle.dump({"weights": WEIGHTS, "vectorizers": vectorizer_info}, f)

    print(f"Training complete: {len(catalog):,} movies")
    print(f"Saved artifacts to: {ARTIFACT_DIR}")
    print("Feature weights:", WEIGHTS)
    print("Next: streamlit run app.py")


if __name__ == "__main__":
    main()
