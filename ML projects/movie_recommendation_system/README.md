# 🎬 Movie Recommendation System

A content-based movie recommendation system built using **Python, Machine Learning, Streamlit, and the TMDB 5000 dataset**.

The application recommends movies based on their metadata, including genres, keywords, overview, cast, and director. It uses **CountVectorizer and Cosine Similarity** with weighted features to calculate movie similarity.

## 🚀 Features

- **Content-Based Recommendations:** Recommends movies based on their content and metadata.
- **Feature Weighting:** Assigns different importance to genres, keywords, overview, cast, and director.
- **Text Preprocessing:** Includes lowercasing, punctuation cleaning, stemming, and duplicate-token removal.
- **Movie Posters:** Fetches movie posters using the TMDB API.
- **Interactive UI:** Built with Streamlit for an easy-to-use experience.
- **Movie Information:** Displays genres, overview, and recommended movies.
- **Similarity Scores:** Option to inspect similarity scores for recommendations.

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- SciPy
- NLTK
- Streamlit
- TMDB API
- Jupyter Notebook

## 🧠 How It Works

The recommendation system follows these steps:

1. **Data Collection:** Uses the TMDB 5000 Movies and Credits datasets.
2. **Data Preprocessing:** Extracts relevant movie information, including genres, keywords, cast, director, and overview.
3. **Text Cleaning:** Applies lowercasing, stemming, and duplicate-token removal.
4. **Feature Extraction:** Converts text metadata into numerical vectors using CountVectorizer.
5. **Feature Weighting:** Assigns different weights to metadata categories to influence their contribution to similarity.
6. **Similarity Calculation:** Uses Cosine Similarity to calculate similarity between movies.
7. **Recommendation:** Returns the top similar movies based on the selected movie.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Download the TMDB 5000 Movies and Credits datasets and place both CSV files inside the `data/` directory.

Required files:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 5. Train the recommendation model

Run:

```bash
python train_model.py
```

This generates the required model artifacts inside the `artifacts/` directory.

### 6. Configure TMDB API

Create a file named `.streamlit/secrets.toml` and add your TMDB API key:

```toml
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
```

Keep your API key private. Never commit your secrets file to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📂 Project Structure

```text
movie-recommendation-system/
│
├── app.py
├── train_model.py
├── evaluate_recommendations.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── artifacts/
│   ├── movie_catalog.pkl
│   └── similarity.pkl
│
└── .streamlit/
    └── secrets.toml
```

## 📊 Recommendation Evaluation

Run the evaluation script:

```bash
python evaluate_recommendations.py
```

It displays recommended movie titles, genres, and similarity scores for manual inspection.

Similarity scores represent textual similarity, not guaranteed user preference or recommendation accuracy.

## 🔮 Future Improvements

- Experiment with different feature weights.
- Explore TF-IDF and semantic embeddings.
- Improve recommendation relevance through systematic evaluation.
- Add user ratings and personalized recommendations.
- Deploy the application online.

 

*This project was developed as a practical implementation of content-based recommendation techniques and machine learning concepts.*