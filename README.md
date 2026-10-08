# Movie Recommender (content-based)

A small Flask web app that recommends five movies similar to one you pick. Similarity is
content-based: it compares each film's genres, keywords, top cast, director and plot overview.

## How it works
1. **Data:** TMDB 5000 Movies + Credits (Kaggle), merged on title. Not included in this repo (`analysis.ipynb` expects them in `data/`).
2. **Cleaning:** parsed the JSON-style columns (`genres`, `keywords`, `cast`, `crew`) with `ast.literal_eval`, kept the top 5 cast members and the director, dropped rows with missing values.
3. **Features:** combined overview, genres, keywords, cast and director into one "tags" text field, lemmatised it (NLTK WordNet) and vectorised it with `CountVectorizer` (500 features, English stop words removed).
4. **Similarity:** cosine similarity between every pair of films, saved with the movie table as `similarity.pkl` / `model.pkl`.
5. **App:** `app.py` looks up the chosen film's row in the similarity matrix and returns the five highest-scoring other films.

The saved model covers **1,489 titles**.

## Run it
```bash
pip install -r requirements.txt
python app.py        # then open http://127.0.0.1:5000
```
To rebuild the model, run `analysis.ipynb` (also needs `scikit-learn`, `nltk`, and the two TMDB CSVs).

## Limitations
- Content-based only: no user ratings, so no personalisation.
- No quantitative evaluation: recommendations were checked by eye, not against a metric.
- Bag-of-words features ignore word order and meaning; embeddings or TF-IDF would likely do better.

## Bug fix note
`dropna()` leaves gaps in the DataFrame's row labels, but the similarity matrix is indexed by row *position*.
The index is now reset (`reset_index(drop=True)`) in the notebook and when the app loads the model;
without it, recommendations for most titles came from the wrong row.
