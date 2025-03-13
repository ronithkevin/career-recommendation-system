import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

function App() {
    const [interests, setInterests] = useState("");
    const [recommendation, setRecommendation] = useState("");
    const [loading, setLoading] = useState(false);

    const getRecommendation = async () => {
        setLoading(true);
        try {
            const response = await axios.post("http://127.0.0.1:5000/recommend", { interests });
            setRecommendation(response.data.career_recommendation);
        } catch (error) {
            setRecommendation("Error fetching recommendation.");
        }
        setLoading(false);
    };

    return (
        <div className="container">
            <h2>Career Recommendation System</h2>
            <input
                type="text"
                placeholder="Enter your skills (e.g., Python, AI, Machine Learning)"
                value={interests}
                onChange={(e) => setInterests(e.target.value)}
            />
            <button onClick={getRecommendation} disabled={loading}>
                {loading ? "Loading..." : "Get Recommendation"}
            </button>
            <p className="result">{recommendation}</p>
        </div>
    );
}

export default App;
