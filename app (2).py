from flask import Flask, render_template, request
#Flask creates the web application, render_template sends an HTML file to the browser, request lets Flask read data sent from the browser to form the input 
import os
import pickle 

print("Starting app...")

app = Flask(__name__) #initialises Flask application, main file

#load saved model data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies = pickle.load(open(os.path.join(BASE_DIR, 'model.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb')) #rb = read binary 

#copying in the recommend function from analysis.ipnyb 
#recommendation function 
def get_recommendations(movie_title, top_n=5):
    movie_index = movies[movies['title'] == movie_title].index[0] #selects the index of the selected movie
    scores = similarity[movie_index] #turns 2D array of similarity into a 1D array (similarity of selected movie with other movies)
    indexed_scores = list(enumerate(scores)) #pairs each similarity score with its movie index and turns it into a list
    movie_list = sorted(indexed_scores, key=lambda x:x[1], reverse=True) #sorts the list into (movie_index, similarity_score) and sorts using the similarity score, not the index 
    #reverse = True -> use descending sorting (largest similarity first)
#creating the home page 

    recommended_movies = movie_list[1:top_n+1] #excluding the movie itself, pick the top n similar movies
    return [movies.iloc[i[0]].title for i in recommended_movies] #i[0] = movie index, gets the title according to the movie index

@app.route('/')
def home():
    movie_titles = movies['title'].values #extracts all movie titles 
    return render_template('index.html', movie_titles=movie_titles) #sends the movie titles to index.html, html_variable_name=python_value

@app.route('/recommend', methods=['POST']) #this route only runs when the form is submitted  

def recommend():
    movie_title = request.form['movie'] #ask user for a movie they like 
    recommendations = get_recommendations(movie_title)

    return render_template( #sends these following variables to HTML
        'index.html',
        movie_titles=movies['title'].values, #list of all movie titles
        selected_movie=movie_title,
        recommendations=recommendations
    )

if __name__ == '__main__':
    app.run(debug=True)

