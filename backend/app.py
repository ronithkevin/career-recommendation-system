from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Sample dataset: Career options mapped to skills/interests
career_data = {
    "Software Engineer": "programming coding algorithms data structures problem-solving",
    "Data Scientist": "data analysis machine learning statistics python",
    "AI Engineer": "deep learning neural networks machine learning AI python",
    "UI/UX Designer": "design creativity user experience prototyping Figma",
    "Cybersecurity Analyst": "security networks encryption ethical hacking penetration testing",
    "Cloud Engineer": "AWS cloud computing DevOps Kubernetes networking",
    "Product Manager": "business strategy leadership market analysis decision-making"
}

# Convert dictionary to DataFrame
df = pd.DataFrame(list(career_data.items()), columns=["Career", "Skills"])

# Text vectorization using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Skills"])

def recommend_career(user_interests):
    """Find the best career match based on user interests using Cosine Similarity."""
    user_vector = vectorizer.transform([user_interests])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_match_index = np.argmax(similarities)
    
    if similarities[top_match_index] > 0:  # Ensure some relevance
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
