from flask import Flask, render_template, request
# Flask creates the web app, render_template sends an HTML file to the browser,
# request lets Flask read the data submitted from the form
import os
import pickle

app = Flask(__name__)  # initialises the Flask application

# ---- load the saved model data ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'model.pkl'), 'rb') as f:
    movies = pickle.load(f)        # DataFrame: id, title, tags, popularity
with open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb') as f:
    similarity = pickle.load(f)    # cosine-similarity matrix (n_movies x n_movies)

# The similarity matrix is indexed by POSITION (row 0, 1, 2, ...), but dropna() in the
# notebook left gaps in the DataFrame's row labels. Resetting the index makes label == position,
# otherwise recommendations are looked up in the wrong row of the matrix.
movies = movies.reset_index(drop=True)


def get_recommendations(movie_title, top_n=5):
    """Return the top_n most similar movie titles (excluding the movie itself)."""
    matches = movies[movies['title'] == movie_title]
    if matches.empty:
        return []                                     # unknown title
    movie_index = matches.index[0]                    # row position of the selected movie
    scores = list(enumerate(similarity[movie_index])) # (movie_index, similarity_score) pairs
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)  # most similar first
    top = ranked[1:top_n + 1]                         # skip [0]: the movie itself
    return [movies.iloc[i].title for i, _ in top]


@app.route('/')
def home():
    return render_template('index.html', movie_titles=movies['title'].values)


@app.route('/recommend', methods=['POST'])  # only runs when the form is submitted
def recommend():
    movie_title = request.form['movie']
    return render_template(
        'index.html',
        movie_titles=movies['title'].values,
        selected_movie=movie_title,
        recommendations=get_recommendations(movie_title),
    )


if __name__ == '__main__':
    app.run(debug=True)
