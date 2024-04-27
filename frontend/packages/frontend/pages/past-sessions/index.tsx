import * as React from "react";
import Skeleton from "@mui/material/Skeleton";
import Stack from "@mui/material/Stack";
// import VideoView from "@/components/PracticeSession/VideoView";
import { Box, Typography } from "@mui/material";
import PracticeSessionsTable from "@/components/Tables/PracticeSessionsTable";

const sessionData = [
  {
    name: "Data Scientist",
    type: "Mock Interview",
    date: "2024-08-26",
    avgScore: 75,
    status: "Processing",
    duration: "3 mins",
    imageSrc: "dataScientist.jpg",
  },
  {
    name: "Frontend React Developer",
    type: "Mock Interview",
    date: "2024-08-23",
    avgScore: 88,
    status: "Analyzed",
    duration: "5 mins",
    imageSrc: "/react.jpg",
  },
  {
    name: "WePrep Pitch",
    type: "Sales Pitch",
    date: "2024-08-25",
    avgScore: 65,
    status: "Analyzed",
    duration: "3 mins",
    imageSrc: "/ps2.jpg",
  },
  {
    name: "WePrep Pitch",
    type: "Sales Pitch",
    date: "2024-08-25",
    avgScore: 42,
    status: "Analyzed",
    duration: "2 mins",
    imageSrc: "/ps1.jpg",
  },
  {
    name: "Presentation Recording",
    type: "Upload Video",
    date: "2021-08-12",
    avgScore: 92,
    status: "Analyzed",
    duration: "6 mins",
    imageSrc: "/ps2.jpg",
  },
  {
    name: "Frontend React Developer",
    type: "Mock Interview",
    date: "2024-08-23",
    avgScore: 83,
    status: "Analyzed",
    duration: "5 mins",
    imageSrc: "/ps1.jpg",
  },
  {
    name: "Frontend React Developer",
    type: "Mock Interview",
    date: "2024-08-23",
    avgScore: 26,
    status: "Analyzed",
    duration: "5 mins",
    imageSrc: "/react.jpg",
  },
];

export default function PracticeSession() {
  return (
    <>
      <Typography variant="h2" align="center" gutterBottom>
        Past Sessions
      </Typography>

      <PracticeSessionsTable data={sessionData} />
    </>
  );
}
