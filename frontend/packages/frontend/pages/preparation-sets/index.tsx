import * as React from "react";
import Skeleton from "@mui/material/Skeleton";
import Stack from "@mui/material/Stack";
// import VideoView from "@/components/PracticeSession/VideoView";
import { Box, Button, Typography } from "@mui/material";
import PreparationSetTable from "@/components/Tables/PreparationSetTable";
import { PlayCircle } from "@mui/icons-material";

const sessionData = [
  {
    name: "Data Scientist",
    type: "Mock Interview",
    date: "2024-08-26",
    avgScore: 75,
    status: "Processing",
    duration: "3 mins",
    sessionCount: 1,
    imageSrc: "dataScientist.jpg",
  },
  {
    name: "Frontend React Developer",
    type: "Mock Interview",
    date: "2024-08-23",
    avgScore: 75,
    sessionCount: 1,
    status: "Analyzed",
    duration: "5 mins",
    imageSrc: "/react.jpg",
  },
  {
    name: "Jane Smith",
    type: "Video Upload",
    date: "2024-08-23",
    avgScore: 88,
    sessionCount: 3,
    status: "Analyzed",
    duration: "15 mins",
    imageSrc: "/ps1.jpg",
  },
  {
    name: "William Johnson",
    type: "Sales Pitch",
    date: "2024-08-25",
    avgScore: 65,
    status: "Analyzed",
    sessionCount: 2,
    duration: "3 mins",
    imageSrc: "/ps2.jpg",
  },
];

export default function PracticeSession() {
  return (
    <>
      <Typography variant="h2" align="center" gutterBottom>
        Preparation Sets
      </Typography>
      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-end",
          marginBottom: "20px",
          marginRight: "20px",
        }}
      >
        <Button
          size="large"
          variant="contained"
          sx={{ textTransform: "none", height: "fit-content" }}
          startIcon={<PlayCircle style={{ fill: "#fff" }} />}
        >
          Create New Preparation Set
        </Button>
      </Box>
      <PreparationSetTable data={sessionData} />
    </>
  );
}
