import * as React from "react";
import Skeleton from "@mui/material/Skeleton";
import Stack from "@mui/material/Stack";
// import VideoView from "@/components/PracticeSession/VideoView";
import { Box, Button, Typography } from "@mui/material";
import PreparationSetTable from "@/components/Tables/PreparationSetTable";
import { PlayCircle } from "@mui/icons-material";

const sessionData = [
  {
    name: "John Doe",
    type: "Mock Interview",
    date: "2021-08-01",
    avgScore: 75,
    status: "Processing",
    duration: "45 mins",
  },
  {
    name: "Jane Smith",
    type: "Mock Interview",
    date: "2021-07-25",
    avgScore: 88,
    status: "Analyzed",
    duration: "30 mins",
  },
  {
    name: "William Johnson",
    type: "Sales Pitch",
    date: "2021-06-17",
    avgScore: 65,
    status: "Processing",
    duration: "1 hour",
  },
  {
    name: "Amanda Brown",
    type: "Mock Interview",
    date: "2021-08-12",
    avgScore: 92,
    status: "Analyzed",
    duration: "2 hours",
  },
  {
    name: "Matthew Garcia",
    type: "Presentation Practice",
    date: "2021-05-09",
    avgScore: 78,
    status: "Analyzed",
    duration: "1.5 hours",
  },
  {
    name: "Samantha Miller",
    type: "Video Upload",
    date: "2021-04-22",
    avgScore: 59,
    status: "Analyzed",
    duration: "50 mins",
  },
  {
    name: "Ethan Davis",
    type: "Video Upload",
    date: "2021-03-15",
    avgScore: 81,
    status: "Processing",
    duration: "40 mins",
  },
  {
    name: "Sophia Rodriguez",
    type: "Quick Start",
    date: "2021-02-05",
    avgScore: 85,
    status: "Processing",
    duration: "1 hour 15 mins",
  },
  {
    name: "James Wilson",
    type: "Quick Start",
    date: "2021-01-30",
    avgScore: 45,
    status: "Processing",
    duration: "35 mins",
  },
  {
    name: "Olivia Martinez",
    type: "Sales Pitch",
    date: "2021-01-12",
    avgScore: 90,
    status: "Analyzed",
    duration: "55 mins",
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
