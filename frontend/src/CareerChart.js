import React from "react";
import { Bar } from "react-chartjs-2";

const CareerChart = ({ careerData }) => {
    const data = {
        labels: careerData.map(career => career.name),
        datasets: [
            {
                label: "Career Popularity",
                data: careerData.map(career => career.count),
                backgroundColor: "rgba(54, 162, 235, 0.6)",
            }
        ]
    };

    return (
        <div>
            <h3>Career Trends</h3>
            <Bar data={data} />
        </div>
    );
};

export default CareerChart;
