"""Print recommendations and similarity scores for quick manual quality checks."""
from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"

with open(ARTIFACT_DIR / "movie_catalog.pkl", "rb") as f:
    catalog = pickle.load(f)
with open(ARTIFACT_DIR / "similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

def inspect(movie_title, top_n=10):
    matches = catalog.index[catalog["title"].str.casefold() == movie_title.casefold()].tolist()
    if not matches:
        print(f"Movie not found: {movie_title}")
        return
    index = matches[0]
    ranked = sorted(
        enumerate(similarity[index]),
        key=lambda pair: float(pair[1]),
        reverse=True
    )
    print(f"\nRecommendations for: {catalog.iloc[index]['title']}")
    shown = 0
    for movie_index, score in ranked:
        if movie_index == index:
            continue
        row = catalog.iloc[movie_index]
        genres = ", ".join(row["genres_list"] or [])
        print(f"{score:.4f} | {row['title']} | {genres}")
        shown += 1
        if shown >= top_n:
            break

if __name__ == "__main__":
    while True:
        title = input("\nEnter a movie title (or q to quit): ").strip()
        if title.lower() in {"q", "quit", "exit"}:
            break
        inspect(title)
