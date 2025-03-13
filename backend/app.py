from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Load dataset
df = pd.read_csv("career_data.csv")

# Vectorize career data
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Skills"])

def recommend_career(user_interests):
    """Find the best career match using Cosine Similarity."""
    user_vector = vectorizer.transform([user_interests])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_match_index = np.argmax(similarities)
    
    if similarities[top_match_index] > 0:
        return df.iloc[top_match_index]["Career"]
    return "No strong career match found."

@app.route('/recommend', methods=['POST'])
def recommend():
    """API Endpoint for career recommendations."""
    data = request.json
    interests = data.get("interests", "").strip()
    if not interests:
        return jsonify({"error": "Please provide your interests"}), 400
    return jsonify({"career_recommendation": recommend_career(interests)})

if __name__ == '__main__':
    app.run(debug=True)
