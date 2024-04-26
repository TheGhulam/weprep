import React from "react";
import { Radar } from "react-chartjs-2";
import { Chart, LineElement, PointElement, RadialLinearScale } from "chart.js"


Chart.register(RadialLinearScale, PointElement, LineElement)

// Define the data structure for an individual entity's scores
interface Score {
  label: string; // Name of the entity
  score: number; // Scores for each metric
}

interface RadarChartProps {
  scores: Score[]; // Array of entities with their scores
}

const PerformanceRadarChart: React.FC<RadarChartProps> = ({ scores }) => {
    
    const titles = scores.map(scores => scores.label)
    const points = scores.map(scores => scores.score)

    // Transform the data into the format expected by Chart.js
    const data = {
        labels: titles,
        datasets: [{
            data: points,
            backgroundColor: "rgba(54, 162, 235, 0.2)", // Blue color with transparency
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1
        }]
        

    };

    // Define options for the radar chart
    const options = {
        scales: {
            r: {
                min: 0,
                max: 100, // Adjust this value based on your score range
                stepSize: 10,
            },
        },
    };

    return <Radar data={data} options={options} />;
};

export default PerformanceRadarChart;