from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///careers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define database model
class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    career_name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Load career data from the database
def get_career_data():
    careers = Career.query.all()
    return [{"Career": c.career_name, "Skills": c.skills} for c in careers]

# Train TF-IDF Model
def train_model():
    career_data = get_career_data()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([c["Skills"] for c in career_data])
    return vectorizer, tfidf_matrix, career_data

vectorizer, tfidf_matrix, career_data = train_model()

def recommend_career(user_interests):
    user_vector = vectorizer.transform([user_interests])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_match_index = similarities.argmax()
    
    if similarities[top_match_index] > 0:
        return career_data[top_match_index]["Career"]
    return "No strong career match found."

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    interests = data.get("interests", "").strip()
    if not interests:
        return jsonify({"error": "Please provide your interests"}), 400
    return jsonify({"career_recommendation": recommend_career(interests)})

if __name__ == '__main__':
    app.run(debug=True)
