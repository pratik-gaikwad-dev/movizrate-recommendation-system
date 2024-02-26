from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

with open('models/cosine.pkl', 'rb') as file:
    cosine_sim = pickle.load(file)
    
with open('models/tfidf.pkl', 'rb') as file:
    tfidf_vectorizer = pickle.load(file)
    
with open('models/data.pkl', 'rb') as file:
    data = pickle.load(file)

# Function to get movie recommendations based on movie_title
def get_recommendations(movie_title, cosine_sim=cosine_sim):
    idx = data[data['name'] == movie_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar movies (excluding itself)
    movie_indices = [i[0] for i in sim_scores]
    return data['name'].iloc[movie_indices]

# Define an endpoint for movie recommendations
@app.route('/recommendations', methods=['GET'])
def recommend_movies():
    movie_title = request.args.get('movie_title')
    if movie_title is not None:
        recommended_movies = get_recommendations(movie_title)
        return jsonify({'recommendations': recommended_movies.tolist()})
    else:
        return jsonify({'error': 'Please provide a movie_title parameter.'})

if __name__ == '__main__':
    app.run(debug=True)
