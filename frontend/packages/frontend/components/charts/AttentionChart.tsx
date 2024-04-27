// components/AttentionChart.tsx
import React from "react";
import dynamic from "next/dynamic";
import { useTheme } from "@mui/material";

const ReactApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

const attentionData = [
  {
    name: "Attention",
    data: [
      70, 65, 75, 70, 85, 80, 60, 65, 70, 65, 85, 78, 55, 60, 65, 70, 80, 75, 50, 55, 60, 75, 85,
      70, 45, 50, 55, 70, 90, 80,
    ],
  },
];

const AttentionChart = () => {
  const theme = useTheme();

  const options = {
    chart: {
      height: 350,
      type: "line",
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
      animations: {
        enabled: true,
        easing: "easeinout",
        speed: 800,
        animateGradually: {
          enabled: true,
          delay: 150,
        },
        dynamicAnimation: {
          enabled: true,
          speed: 350,
        },
      },
    },
    annotations: {
      xaxis: [
        { x: "0:00", x2: "0:16", fillColor: "transparent", label: { text: "Intro" } },
        {
          x: "0:16",
          x2: "0:48",
          fillColor: "#97C2F9",
          label: { text: "Q1" },
        },
        { x: "0:48", x2: "1:20", fillColor: "transparent", label: { text: "Q2" } },
        {
          x: "1:20",
          x2: "2:00",
          fillColor: "#97C2F9",
          label: { text: "Q3" },
        },
        { x: "2:00", x2: "2:40", fillColor: "transparent", label: { text: "Q4" } },
        {
          x: "2:40",
          x2: "3:15",
          fillColor: "#97C2F9",
          label: { text: "Q5" },
        },
      ],
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
    },
    xaxis: {
      type: "category",
      categories: [
        "0:00",
        "0:08",
        "0:16",
        "0:24",
        "0:32",
        "0:40",
        "0:48",
        "0:56",
        "1:04",
        "1:12",
        "1:20",
        "1:28",
        "1:36",
        "1:44",
        "1:52",
        "2:00",
        "2:08",
        "2:16",
        "2:24",
        "2:32",
        "2:40",
        "2:48",
        "2:56",
        "3:04",
        "3:15",
      ],
      labels: {
        style: {
          colors: theme.palette.text.primary,
        },
      },
    },
    yaxis: {
      title: {
        text: "Attention Level (%)",
        style: {
          color: theme.palette.text.primary,
        },
      },
      labels: {
        style: {
          color: theme.palette.text.primary,
        },
      },
    },
    title: {
      align: "left",
      style: {
        color: theme.palette.text.primary,
      },
    },
  };

  return (
    <div>
      <ReactApexChart options={options} series={attentionData} type="line" height={350} />
    </div>
  );
};

export default AttentionChart;
