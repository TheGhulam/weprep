import React from "react";
import Chart from "react-apexcharts";

const AudioChart = () => {
  const interpolateData = (data, times) => {
    const newData = [];
    const newTimes = [];
    for (let i = 0; i < data.length - 1; i++) {
      const startData = data[i];
      const endData = data[i + 1];
      const startTime = times[i];
      const endTime = times[i + 1];
      const steps = 5;
      const stepSizeData = (endData - startData) / steps;
      const stepSizeTime = (endTime - startTime) / steps;

      newData.push(startData);
      newTimes.push(startTime);
      for (let j = 1; j < steps; j++) {
        newData.push(Math.round((startData + stepSizeData * j) * 10) / 10);
        newTimes.push(startTime + stepSizeTime * j);
      }
    }
    newData.push(data[data.length - 1]);
    newTimes.push(times[times.length - 1]);
    return { newData, newTimes };
  };

  const options = {
    chart: {
      height: 350,
      type: "line",
      zoom: {
        enabled: false,
      },
      toolbar: {
        show: true,
      },
    },
    annotations: {
      xaxis: [
        { x: 0, x2: 16, fillColor: "transparent", label: { text: "Intro" } },
        { x: 16, x2: 48, fillColor: "#97C2F9", label: { text: "Q1" } },
        { x: 48, x2: 80, fillColor: "transparent", label: { text: "Q2" } },
        { x: 80, x2: 120, fillColor: "#97C2F9", label: { text: "Q3" } },
        { x: 120, x2: 160, fillColor: "transparent", label: { text: "Q4" } },
        { x: 160, x2: 195, fillColor: "#97C2F9", label: { text: "Q5" } },
      ],
    },
    xaxis: {
      type: "numeric",
      tickAmount: 10,
      labels: {
        formatter: (val) => `${Math.floor(val / 60)}:${("0" + Math.floor(val % 60)).slice(-2)}`,
      },
    },
    stroke: {
      width: 2,
      curve: "smooth",
    },
    dataLabels: {
      enabled: false,
    },
    title: {
      text: "Audio Analysis",
      align: "left",
    },
    markers: {
      size: 3,
      hover: {
        sizeOffset: 6,
      },
    },
    tooltip: {
      x: {
        show: true,
      },
    },
  };

  const originalData = [
    {
      name: "Pitch",
      data: [0, 0, 5, 4, 6, 0, 6, 7, 0, 8, 8, 0, 2, 6, 0, 5, 0],
      times: [0, 15, 16, 30, 45, 48, 60, 75, 80, 95, 110, 120, 135, 150, 160, 175, 185], // Corresponding times in seconds
    },
    {
      name: "Volume",
      data: [0, 0, 4, 3, 4, 0, 5, 6, 0, 6, 7, 0, 4, 3, 0, 6, 0],
      times: [0, 15, 16, 30, 45, 48, 60, 75, 80, 95, 110, 120, 135, 150, 160, 175, 185],
    },
    {
      name: "Clarity",
      data: [0, 0, 7, 8, 6, 0, 7, 8, 0, 8, 9, 0, 8, 6, 0, 7, 0],
      times: [0, 15, 16, 30, 45, 48, 60, 75, 80, 95, 110, 120, 135, 150, 160, 175, 185],
    },
  ];

  const series = originalData.map((series) => {
    const { newData, newTimes } = interpolateData(series.data, series.times);
    return {
      name: series.name,
      data: newData.map((value, index) => ({ x: newTimes[index], y: value })),
    };
  });

  return (
    <div>
      <Chart options={options} series={series} type="line" height={350} />
    </div>
  );
};

export default AudioChart;
