import React from "react";
import { Box, Grid, Typography, Button } from "@mui/material";
import PracticeGuide from "@/components/PracticeGuides/PracticeGuide";

const recommendations = [
  {
    title: "Learn STAR Method of Answering Questions",
    ytLink1: "https://www.youtube.com/watch?v=uQEuo7woEEk",
    ytLink2: "https://www.youtube.com/watch?v=ZSSID5mp93o",
    ytLink3: "https://www.youtube.com/watch?v=8QfSnuL8Ny8",
  },
  {
    title: "Advanced State Management with Redux",
    ytLink1: "https://www.youtube.com/watch?v=k1MOFQBecnE",
    ytLink2: "https://www.youtube.com/watch?v=JkBi7l_6mEA",
    ytLink3: "https://www.youtube.com/watch?v=rtwZrbpsbIY",
  },
  {
    title: "Effective Unit Testing in React",
    ytLink1: "https://www.youtube.com/watch?v=JBSUgDxICg8",
    ytLink2: "https://www.youtube.com/watch?v=OVNjsIto9xM",
    ytLink3: "https://www.youtube.com/watch?v=Xq4YmngRxxg",
  },
  {
    title: "Practice Word Pacing",
    ytLink1: "https://www.youtube.com/watch?v=032Hum9KNjw",
    ytLink2: "https://www.youtube.com/watch?v=S2nFK_fLhu4",
    ytLink3: "https://www.youtube.com/watch?v=PlJaaUYIwIM",
  },
];

export default function AnalyticsPage() {
  return (
    <>
      <Typography variant="h2" align="center" gutterBottom>
        Training Roadmap
      </Typography>
      <PracticeGuide guides={recommendations} />
    </>
  );
}
