// components/ApexChart.tsx
import React from "react";
import dynamic from "next/dynamic";
import { useTheme } from "@mui/material";
const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

const videoData = [
  { name: "Fear", data: [5, 4, 4, 6, 4, 4, 8, 9, 1] }, // Lowered as fear would be less common in a standard interview.
  { name: "Sad", data: [20, 15, 16, 8, 3, 0, 0, 0, 0] }, // Reduced because sadness might not be strongly expressed.
  { name: "Neutral", data: [40, 50, 60, 55, 50, 45, 50, 40, 35] }, // Increased and more constant as neutrality is common.
  { name: "Angry", data: [2, 3, 9, 0, 0, 0, 0, 1, 0] }, // Very low as anger is less likely in a controlled interview environment.
  { name: "Surprise", data: [1, 0, 2, 1, 0, 1, 0, 0, 1] }, // Occasional surprises might occur, depending on the interview questions.
  { name: "Happy", data: [1, 4, 6, 8, 12, 20, 17, 8, 7] }, // More frequent happy responses due to positive interactions.
  { name: "Disgust", data: [8, 6, 0, 1, 8, 0, 0, 0, 0] }, // Minimal, as disgust would rarely occur unless provoked.
];

const FacialEmotionChart = () => {
  const theme = useTheme();

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
      labels: {
        style: {
          colors: theme.palette.text.primary, // Applying text color from theme
        },
      },
    },
    yaxis: {
      title: {
        text: "Percentage",
        style: {
          color: theme.palette.text.primary, // Applying text color from theme
        },
      },
      labels: {
        style: {
          color: theme.palette.text.primary, // Applying text color from theme
        },
      },
    },
    title: {
      style: {
        color: theme.palette.text.primary, // Applying text color from theme
      },
    },
  };

  return (
    <div>
      <ReactApexChart options={options} series={videoData} type="line" height={350} />
    </div>
  );
};

export default FacialEmotionChart;
