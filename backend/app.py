from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

app = Flask(__name__)

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

# Load career dataset from CSV
df = pd.read_csv("career_data.csv")

# Text vectorization using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Skills"])

def recommend_career(user_interests):
    """Find the best career match based on user interests using Cosine Similarity."""
    user_vector = vectorizer.transform([user_interests])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_match_index = np.argmax(similarities)
    
    if similarities[top_match_index] > 0:
        return df.iloc[top_match_index]["Career"]
    return "No strong career match found. Try refining your skills."

@app.route('/recommend', methods=['POST'])
def recommend():
    """API Endpoint to get career recommendations."""
    data = request.json
    interests = data.get("interests", "").strip()
    
    if not interests:
        return jsonify({"error": "Please provide your interests"}), 400
    
    career_suggestion = recommend_career(interests)
    return jsonify({"career_recommendation": career_suggestion})

if __name__ == '__main__':
    app.run(debug=True)
