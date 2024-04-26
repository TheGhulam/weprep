// components/ApexChart.tsx
import React from "react";
import dynamic from "next/dynamic";
const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

const emotionData = [
  { name: "Happy", data: [5, 10, 15, 20, 18, 24, 30, 25, 20] },
  { name: "Sad", data: [10, 15, 10, 5, 8, 4, 5, 2, 1] },
  { name: "Angry", data: [3, 4, 5, 3, 2, 1, 1, 1, 0] },
  { name: "Fearful", data: [1, 2, 1, 3, 4, 5, 6, 7, 8] },
  { name: "Surprise", data: [0, 1, 1, 2, 2, 3, 3, 4, 4] },
  { name: "Disgust", data: [0, 0, 1, 1, 1, 0, 0, 0, 0] },
  { name: "Calm", data: [20, 18, 15, 10, 5, 4, 3, 2, 1] },
  { name: "Neutral", data: [50, 40, 30, 20, 10, 5, 3, 2, 1] },
];

const options = {
  chart: {
    height: 350,
    type: "line",
    zoom: {
      enabled: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
  },
  xaxis: {
    categories: ["0:00", "0:25", "0:50", "1:15", "1:40", "2:05", "2:30", "2:55", "3:15"],
  },
  yaxis: {
    title: {
      text: "Percentage",
    },
  },
};

const AllEmotionChart = () => (
  <div>
    <ReactApexChart options={options} series={emotionData} type="line" height={350} />
  </div>
);

export default AllEmotionChart;
