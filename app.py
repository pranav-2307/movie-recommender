from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie dataset
movies = pd.read_csv('tmdb_5000_movies.csv')
movies = movies[['title', 'overview']].dropna()

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['overview'])
similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def get_recommendations(title):
    try:
        idx = movies[movies['title'].str.lower() == title.lower()].index[0]
        sim_scores = list(enumerate(similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
        movie_indices = [i[0] for i in sim_scores]
        return movies['title'].iloc[movie_indices].tolist()
    except IndexError:
        return ["Movie not found. Please try another title."]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie = data.get('movie', '')
    recommendations = get_recommendations(movie)
    return jsonify({'recommendations': recommendations})

@app.route('/titles', methods=['GET'])
def titles():
    titles = movies['title'].tolist()
    return jsonify(titles)

if __name__ == '__main__':
    app.run(debug=True)
