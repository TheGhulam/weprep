import React from "react";
import { Typography, Grid, Box, useTheme } from "@mui/material";
import CircularScore from "@/components/analytics/CircularScore";
import Calendar from "react-github-contribution-calendar";
import { alignProperty } from "@mui/material/styles/cssUtils";
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
export default function BasicCard() {
  const theme = useTheme();
  var values = {
    "2023-07-23": 1,
    "2024-01-26": 2,
    "2024-02-27": 3,
    "2024-01-28": 4,
    "2024-01-29": 4,
    "2024-02-01": 3,
    "2024-02-05": 2,
    "2024-02-15": 1,
    "2024-02-20": 4,
    "2024-03-01": 2,
    "2024-03-05": 3,
    "2024-03-10": 4,
    "2024-03-15": 1,
    "2024-03-20": 2,
    "2024-03-25": 3,
  };
  var until = "2024-03-29";

  var panelColors = [
    theme.palette.mode === "light" ? "#D4D4D8" : "#2D2F39",
    "#E2F1FA",
    "#99C7FB",
    "#2A93D5",
    "#00255A",
  ];

  //   ("#2D2F39");
  var monthLabelAttributes = {
    style: {
      "font-size": 10,
      "alignment-baseline": "central",
      fill: theme.palette.text.secondary,
    },
  };
  var weekLabelAttributes = {
    style: {
      "font-size": 10,
      "alignment-baseline": "central",
      fill: theme.palette.text.secondary,
    },
  };
  var panelAttributes = {
    rx: 3,
    ry: 3,
  };

  return (
    <Box sx={{ width: "100%", overflowX: "auto" }}>
      <Typography variant="h2" align="center" gutterBottom>
        Welcome Faaiz 👋
      </Typography>
      <Typography variant="h3" sx={{ ml: 2, mb: 2 }}>
        Average Scores
      </Typography>
      <Grid container spacing={5} justifyContent="center">
        <Grid item>
          <CircularScore
            label="Confidence Score"
            toolTipInfo="Confidence is the average of your audio, body language..."
            progressScore={89}
          />
        </Grid>
        <Grid item>
          <CircularScore
            label="Clarity Score"
            toolTipInfo="Clarity score reflects how clearly you are able to express your ideas."
            progressScore={52}
          />
        </Grid>
        <Grid item>
          <CircularScore
            label="Filler Word Usage"
            toolTipInfo="Filler word usage counts the unnecessary words or sounds you make."
            progressScore={25}
          />
        </Grid>
        <Grid item>
          <CircularScore
            label="Emotional Score"
            toolTipInfo="Emotional score measures the positivity or negativity of your tone."
            progressScore={74}
          />
        </Grid>
        <Grid item>
          <CircularScore
            label="Attention Score"
            toolTipInfo="Attention score gauges how well you keep your audience engaged."
            progressScore={92}
          />
        </Grid>
        <Grid item>
          <CircularScore
            label="Body Language"
            toolTipInfo="Body language score assesses your non-verbal communication skills."
            progressScore={29}
          />
        </Grid>
        <Grid item>
          <CircularScore
            label="Energy Level"
            toolTipInfo="Energy level score evaluates the vitality and enthusiasm you convey."
            progressScore={50}
          />
        </Grid>
      </Grid>
      <Typography variant="h3" sx={{ ml: 2, mb: 3, mt: 3 }}>
        5 Practice Session this Year
      </Typography>
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
        <Calendar
          monthLabelAttributes={monthLabelAttributes}
          weekLabelAttributes={weekLabelAttributes}
          panelAttributes={panelAttributes}
          values={values}
          until={until}
          panelColors={panelColors}
        />
      </div>
      <Box sx={{ display: "flex", justifyContent: "flex-end", alignItems: "center", mt: 2 }}>
        <Typography variant="body2" sx={{ mr: 1 }}>
          Less
        </Typography>
        {panelColors.map((color, index) => (
          <Box
            key={index}
            sx={{
              width: 17,
              height: 17,
              backgroundColor: color,
              mx: 0.5,
              borderRadius: 1,
            }}
          />
        ))}
        <Typography variant="body2" sx={{ ml: 1 }}>
          More
        </Typography>
      </Box>
      <Typography variant="h3" sx={{ ml: 2, mb: 3, mt: 3 }}>
        Latest Practice Sessions
      </Typography>
      <PracticeSessionsTable data={sessionData} />
    </Box>
  );
}
