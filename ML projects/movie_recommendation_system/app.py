"""Streamlit UI for the improved weighted movie recommender."""
from pathlib import Path
import os
import pickle
import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"

st.set_page_config(page_title="MovieMatch", page_icon="🎬", layout="wide")
st.title("🎬 MovieMatch")
st.caption("Content-based movie recommendations powered by weighted metadata similarity.")

@st.cache_resource
def load_artifacts():
    catalog_path = ARTIFACT_DIR / "movie_catalog.pkl"
    similarity_path = ARTIFACT_DIR / "similarity.pkl"
    if not catalog_path.exists() or not similarity_path.exists():
        return None, None
    # Only load pickle files generated locally by your own train_model.py.
    with open(catalog_path, "rb") as f:
        catalog = pickle.load(f)
    with open(similarity_path, "rb") as f:
        similarity = pickle.load(f)
    return catalog, similarity

def get_api_key():
    try:
        return st.secrets.get("TMDB_API_KEY", "")
    except Exception:
        return os.getenv("TMDB_API_KEY", "")

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_poster(movie_id, api_key):
    if not api_key:
        return None
    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}"
    try:
        response = requests.get(
            url, params={"api_key": api_key}, timeout=12
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except (requests.RequestException, ValueError, TypeError):
        return None
    return None

def get_recommendations(selected_title, catalog, similarity, number=5):
    matches = catalog.index[catalog["title"] == selected_title].tolist()
    if not matches:
        return []
    movie_index = matches[0]
    scores = similarity[movie_index]
    ranked_indices = sorted(
        range(len(scores)), key=lambda idx: float(scores[idx]), reverse=True
    )
    results, seen_ids = [], {int(catalog.iloc[movie_index]["movie_id"])}
    for idx in ranked_indices:
        row = catalog.iloc[idx]
        movie_id = int(row["movie_id"])
        if movie_id in seen_ids:
            continue
        seen_ids.add(movie_id)
        results.append((row, float(scores[idx])))
        if len(results) == number:
            break
    return results

catalog, similarity = load_artifacts()
if catalog is None:
    st.error("Model files are missing. Run `python train_model.py` after placing both CSV files in the data/ folder.")
    st.stop()

if len(catalog) != similarity.shape[0] or similarity.shape[0] != similarity.shape[1]:
    st.error("The catalog and similarity matrix do not match. Run `python train_model.py` again.")
    st.stop()

movie_titles = sorted(catalog["title"].dropna().unique().tolist())
selected_title = st.selectbox("Choose a movie you like", movie_titles)
number = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)
show_scores = st.toggle("Show similarity scores (for debugging)", value=False)

selected_rows = catalog[catalog["title"] == selected_title]
selected = selected_rows.iloc[0]
api_key = get_api_key()

st.subheader("Selected movie")
col1, col2 = st.columns([1, 3])
with col1:
    poster = fetch_poster(selected["movie_id"], api_key)
    if poster:
        st.image(poster, use_container_width=True)
    else:
        st.info("Poster unavailable. Add a valid TMDB API key in .streamlit/secrets.toml.")
with col2:
    st.markdown(f"### {selected['title']}")
    genres = selected["genres_list"] or []
    st.write("**Genres:** " + (", ".join(genres) if genres else "Not available"))
    st.write(selected["overview_display"] or "Overview not available.")

st.divider()
st.subheader("Recommended movies")
recommendations = get_recommendations(selected_title, catalog, similarity, number)

if not recommendations:
    st.warning("No recommendations found for this title.")
else:
    columns = st.columns(5)
    for i, (row, score) in enumerate(recommendations):
        with columns[i % 5]:
            poster = fetch_poster(row["movie_id"], api_key)
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.caption("Poster unavailable")
            st.markdown(f"**{row['title']}**")
            movie_genres = row["genres_list"] or []
            st.caption(", ".join(movie_genres) if movie_genres else "Genre unavailable")
            if show_scores:
                st.caption(f"Similarity: {score:.3f}")
            with st.expander("Overview"):
                st.write(row["overview_display"] or "Overview not available.")

st.caption(
    "Similarity is a text-based score, not a probability or a guarantee that two movies are equally enjoyable."
)
