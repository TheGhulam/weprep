// components/ApexChart.tsx
import React from "react";
import dynamic from "next/dynamic";
import { useTheme } from "@mui/material";
const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

const audioData = [
  { name: "Angry", data: [3, 4, 5, 3, 2, 1, 1, 1, 0] },
  { name: "Happy", data: [5, 10, 15, 20, 18, 24, 30, 25, 20] },
  { name: "Disgust", data: [0, 0, 1, 1, 1, 0, 0, 0, 0] },
  { name: "Surprised", data: [0, 1, 1, 2, 2, 3, 3, 4, 4] },
  { name: "Fearful", data: [1, 2, 1, 3, 4, 5, 6, 7, 8] },
  { name: "Neutral", data: [50, 40, 30, 20, 10, 5, 3, 2, 1] },
  { name: "Sad", data: [10, 15, 10, 5, 8, 4, 5, 2, 1] },
  { name: "Calm", data: [20, 18, 15, 10, 5, 4, 3, 2, 1] },
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
      <ReactApexChart options={options} series={audioData} type="line" height={350} />
    </div>
  );
};

export default FacialEmotionChart;
