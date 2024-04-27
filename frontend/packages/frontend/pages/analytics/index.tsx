import React from "react";
import { Box, Grid, Typography, Button, useTheme } from "@mui/material";
import PerformanceBarChart from "@/components/analytics/PerformanceBar";
import PerformanceRadarChart from "@/components/analytics/PerformanceRadar";
import SpeechAnalysisGrid from "@/components/analytics/SpeechAnalysisGrid";

const videoScores = [
  {
    label: "Eye-Contact",
    score: 54,
  },
  {
    label: "Hand Gestures",
    score: 79,
  },
  {
    label: "Confidence",
    score: 35,
  },
  {
    label: "Engagement",
    score: 60,
  },
  {
    label: "Body Language",
    score: 55,
  },
  {
    label: "Attention",
    score: 70,
  },
];

const videoAreas = [
  {
    title: "Interest",
    avg: 57,
    last: 93,
  },
  {
    title: "Stress",
    avg: 80,
    last: 65,
  },
  {
    title: "Expression",
    avg: 75,
    last: 80,
  },
  {
    title: "Fidgeting",
    avg: 60,
    last: 65,
  },
  {
    title: "Comfort",
    avg: 30,
    last: 60,
  },
];

const audioAreas = [
  {
    title: "Energy Levels",
    avg: 40,
    last: 50,
  },
  {
    title: "Volume",
    avg: 80,
    last: 82,
  },
  {
    title: "Pace",
    avg: 87,
    last: 80,
  },
  {
    title: "Pitch",
    avg: 50,
    last: 62,
  },
  {
    title: "Clarity",
    avg: 30,
    last: 40,
  },
];

const audioScores = [
  {
    label: "Energy Level",
    score: 40,
  },
  {
    label: "Pace",
    score: 80,
  },
  {
    label: "Clarity",
    score: 87,
  },
  {
    label: "Pitch",
    score: 50,
  },
  {
    label: "Tone",
    score: 30,
  },
  {
    label: "Volume",
    score: 60,
  },
];

export default function AnalyticsPage() {
  const theme = useTheme();
  return (
    <>
      <Typography variant="h2" align="center" gutterBottom>
        Analytics
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Box
            // bgcolor={theme.palette.secondary.main}
            p={2}
            border={2}
            borderColor={theme.palette.primary.main}
            borderRadius={6}
          >
            <Typography variant="h2" align="center" gutterBottom>
              Video Analysis
            </Typography>
            <PerformanceRadarChart scores={videoScores} />
            <PerformanceBarChart areas={videoAreas} />
            <Box display="flex" justifyContent="center">
              <Button
                size="large"
                variant="contained"
                sx={{ textTransform: "none", height: "fit-content" }}
              >
                View In-Depth Video Analysis
              </Button>
            </Box>
          </Box>
        </Grid>
        <Grid item xs={6}>
          <Box
            // bgcolor="secondary.light"
            p={2}
            border={2}
            borderColor={theme.palette.primary.main}
            borderRadius={6}
          >
            <Typography variant="h2" align="center" gutterBottom>
              Audio Analysis
            </Typography>
            <PerformanceRadarChart scores={audioScores} />
            <PerformanceBarChart areas={audioAreas} />
            <Box display="flex" justifyContent="center">
              <Button
                size="large"
                variant="contained"
                sx={{ textTransform: "none", height: "fit-content" }}
              >
                View In-Depth Audio Analysis
              </Button>
            </Box>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box
            bgcolor="info.light"
            p={2}
            border={2}
            borderColor={theme.palette.primary.main}
            borderRadius={6}
          >
            <Typography variant="h2" align="center" gutterBottom>
              Speech Analysis
            </Typography>
            <SpeechAnalysisGrid />
            <Box display="flex" justifyContent="center">
              <Button
                size="large"
                variant="contained"
                sx={{ textTransform: "none", height: "fit-content" }}
              >
                View In-Depth Speech Analysis
              </Button>
            </Box>
          </Box>
        </Grid>
      </Grid>
    </>
  );
}
