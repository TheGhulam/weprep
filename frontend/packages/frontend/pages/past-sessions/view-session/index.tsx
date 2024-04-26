import * as React from "react";
import {
  Box,
  Typography,
  Button,
  Stepper,
  Step,
  StepLabel,
  AppBar,
  Tabs,
  Tab,
  Grid,
  Paper,
  StepContent,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ReactPlayer from "react-player";
import { useTheme } from "@mui/material/styles";
import { useRouter } from "next/router";
import TranscriptStepper from "@/components/stepper/TranscriptStepper";
import FeedbackStepper from "@/components/stepper/FeedbackStepper";
import RoadmapStepper from "@/components/stepper/RoadmapStepper";
import AllEmotionChart from "@/components/charts/allEmotionChart";

function SessionDetails() {
  const theme = useTheme();
  const router = useRouter();
  const [activeTab, setActiveTab] = React.useState(0);
  const [activeDetailsTab, setActiveDetailsTab] = React.useState(0);

  const steps = [
    { label: "Finished", description: "Practice Session Finished" },
    { label: "In Progress", description: "Practice Session under AI evaluation" },
    { label: "Analysed", description: "Feedback and Analysis Report Available" },
    {
      label: "Suggested Roadmap",
      description: "Custom Recommendations to continue Improving in this Practice Set",
    },
  ];

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleDetailsTabChange = (event, newValue) => {
    setActiveDetailsTab(newValue);
  };

  const goBack = () => {
    router.push("/past-sessions");
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-start",
          width: "100%",
          padding: 2,
        }}
      >
        <Button
          variant="contained"
          startIcon={<ArrowBackIcon sx={{ fill: "#fff" }} />}
          sx={{ marginRight: 2 }}
          onClick={goBack}
        >
          Back
        </Button>
        <Typography variant="h2" align="center" sx={{ flexGrow: 1 }}>
          Mock Interview Feedback
        </Typography>
      </Box>
      <Stepper activeStep={4} alternativeLabel sx={{ padding: theme.spacing(3) }}>
        {steps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel>{step.label}</StepLabel>
            {/* <StepContent>{step.description}</StepContent> */}
          </Step>
        ))}
      </Stepper>
      <Grid container spacing={2} sx={{ padding: theme.spacing(3) }}>
        <Grid item xs={12} md={6}>
          <ReactPlayer
            url="https://www.youtube.com/watch?v=XclJ3TP4uAU"
            controls={true}
            width="100%"
            height="100%"
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <Tabs value={activeTab} onChange={handleTabChange} aria-label="feedback tabs">
              <Tab label="Transcript" />
              <Tab label="Expert Feedback" />
              <Tab label="Roadmap Suggestions" />
            </Tabs>
          </Box>
          <Box sx={{ maxHeight: 400, overflow: "auto" }}>
            <Typography component="div" role="tabpanel" hidden={activeTab !== 0}>
              <TranscriptStepper />
            </Typography>
            <Typography component="div" role="tabpanel" hidden={activeTab !== 1}>
              <FeedbackStepper />
            </Typography>
            <Typography component="div" role="tabpanel" hidden={activeTab !== 2}>
              <RoadmapStepper />
            </Typography>
          </Box>
        </Grid>
      </Grid>
      <Box sx={{ width: "100%" }}>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Tabs
            value={activeDetailsTab}
            onChange={handleDetailsTabChange}
            aria-label="feedback detail tabs"
          >
            <Tab label="Emotion" />
            <Tab label="Speech" />
            <Tab label="Audio" />
            <Tab label="Video" />
            <Tab label="Accuracy" />
          </Tabs>
        </Box>
        <Box role="tabpanel" hidden={activeDetailsTab !== 0}>
          <AllEmotionChart />
        </Box>
        <Box role="tabpanel" hidden={activeDetailsTab !== 1}>
          Speech details here...
        </Box>
        <Box role="tabpanel" hidden={activeDetailsTab !== 2}>
          Audio details here...
        </Box>
        <Box role="tabpanel" hidden={activeDetailsTab !== 3}>
          Video details here...
        </Box>
        <Box role="tabpanel" hidden={activeDetailsTab !== 4}>
          Accuracy details here...
        </Box>
      </Box>
    </>
  );
}

export default SessionDetails;
