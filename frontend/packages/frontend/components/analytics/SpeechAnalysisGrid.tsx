import React from "react";
import { Grid } from "@mui/material";
import SpeechMetric from "./SpeechMetric"; // Assuming SpeechMetric is the component we discussed earlier

const SpeechAnalysisGrid = () => {
  const metrics = [
    {
      title: "Talking Speed",
      unit: "per minute",
      recommendedMin: 140,
      recommendedMax: 160,
      value: 180, // Example value
      tooltipText: "The optimal range of spoken words per minute for clear understanding.",
    },
    {
      title: "Filler Usage",
      unit: "per 100 words",
      recommendedMin: 7,
      recommendedMax: 10,
      value: 9,
      tooltipText: "Average number of filler words used per 100 words.",
    },
    {
      title: "Question Rate",
      unit: "per minute",
      recommendedMin: 1,
      recommendedMax: 3,
      value: 0,
      tooltipText: "Average number of questions asked per minute during a conversation.",
    },
    {
      title: "Average Patience",
      unit: "seconds",
      recommendedMin: 3,
      recommendedMax: 5,
      value: 8,
      tooltipText: "Average time waited for a response before proceeding.",
    },
    {
      title: "Hedging Words",
      unit: "per 1000 words",
      recommendedMin: 20,
      recommendedMax: 30,
      value: 21,
      tooltipText: "Average use of hedging words to soften statements in a lengthy dialogue.",
    },
    {
      title: "Language Positivity",
      unit: "positivity score",
      recommendedMin: 60,
      recommendedMax: 80,
      value: 30,
      tooltipText: "Measure of positive language tone and expressions.",
    },
    {
      title: "Voice Emotion",
      unit: "emotion level",
      recommendedMin: 50,
      recommendedMax: 70,
      value: 45,
      tooltipText: "Overall emotional tone detected in voice.",
    },
  ];

  return (
    <Grid container spacing={2} mt={1}>
      {metrics.map((metric) => (
        <Grid item xs={12} sm={6} md={4} key={metric.title}>
          <SpeechMetric
            title={metric.title}
            unit={metric.unit}
            recommendedMin={metric.recommendedMin}
            recommendedMax={metric.recommendedMax}
            value={metric.value}
            tooltipText={metric.tooltipText}
          />
        </Grid>
      ))}
    </Grid>
  );
};

export default SpeechAnalysisGrid;
