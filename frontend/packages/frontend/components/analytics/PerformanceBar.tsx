import React from "react";
import { BarChart } from "@mui/x-charts";
import { Box, Typography } from "@mui/material";
import { Label } from "@mui/icons-material";

interface Area {
  title: string;
  avg: number;
  last: number;
}

interface PerformanceBarProps {
  areas: Area[];
}

const PerformanceBarChart: React.FC<PerformanceBarProps> = ({ areas }) => {
  const titles = areas.map((areas) => areas.title);
  const yAxisData = [{ data: titles, scaleType: "band" as const }];

  const avgs = areas.map((areas) => areas.avg);
  const lasts = areas.map((areas) => areas.last);

  const seriesData = [
    { data: avgs, label: "Average Score" },
    { data: lasts, label: "Last Practice Session" },
  ];

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      <BarChart
        series={seriesData}
        height={200}
        yAxis={yAxisData}
        layout="horizontal"
        sx={{ maxWidth: "100%" }}
      />
    </Box>
  );
};

export default PerformanceBarChart;
