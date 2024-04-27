import React from "react";
import Chart from "react-apexcharts";

interface Score {
  label: string; // Name of the entity
  score: number; // Scores for each metric
}

interface RadarChartProps {
  scores: Score[]; // Array of entities with their scores
}

const PerformanceRadarChart: React.FC<RadarChartProps> = ({ scores }) => {
  const titles = scores.map((score) => score.label);
  const points = scores.map((score) => score.score);

  const options = {
    chart: {
      height: 550,
      type: "radar",
    },
    xaxis: {
      categories: titles,
    },
    yaxis: {
      min: 0,
      max: 100, // Adjust this value based on your score range
      tickAmount: 5, // This controls the number of ticks between min and max
    },
    fill: {
      opacity: 0.4,
      colors: ["#36A2EB"],
    },
    stroke: {
      width: 2,
      colors: ["#36A2EB"],
    },
    markers: {
      size: 4,
    },
    tooltip: {
      y: {
        formatter: (val) => `${val}/100`,
      },
    },
  };

  const series = [
    {
      name: "Scores",
      data: points,
    },
  ];

  return (
    <div>
      <Chart options={options} series={series} type="radar" height={350} />
    </div>
  );
};

export default PerformanceRadarChart;
