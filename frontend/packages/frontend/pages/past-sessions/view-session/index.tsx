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
  Tooltip,
  IconButton,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ReactPlayer from "react-player";
import { useTheme } from "@mui/material/styles";
import { useRouter } from "next/router";
import TranscriptStepper from "@/components/stepper/TranscriptStepper";
import FeedbackStepper from "@/components/stepper/FeedbackStepper";
import RoadmapStepper from "@/components/stepper/RoadmapStepper";
import FacialEmotionChart from "@/components/charts/FacialEmotionChart";
import { Book, Info, InfoOutlined } from "@mui/icons-material";
import AudioEmotionChart from "@/components/charts/AudioEmotionChart";
import SpeechAnalysisGrid from "@/components/analytics/SpeechAnalysisGrid";
import AttentionChart from "@/components/charts/AttentionChart";
import AnswerChart from "@/components/charts/AnswerChart";
import AudioChart from "@/components/charts/AudioChart";

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

  const analysisData = [
    {
      tabTitle: "Body Language",
      title: "Body Language and Facial Expressions",
      content: <FacialEmotionChart />,
    },
    {
      tabTitle: "Speech Analysis",
      title: "Speech and Language Analysis",
      content: <SpeechAnalysisGrid />,
    },
    {
      tabTitle: "Vocal Tone",
      title: "Vocal and Speech Tone",
      content: <AudioEmotionChart />,
    },
    {
      tabTitle: "Attention Tracking",
      title: "Attention Levels During Interview",
      content: <AttentionChart />,
    },
    {
      tabTitle: "Audio Analysis",
      title: "Audio Analysis",
      content: <AudioChart />,
    },
    {
      tabTitle: "Answer Analysis",
      title: "Answer and Language Analysis",
      content: <AnswerChart />,
    },
  ];

  const analysisIcons = [
    "Body Language",
    "Speech and Language Analysis",
    "Speech Tone",
    "Attention Tracking",
    "Audio Analysis",
    "Answer Analysis",
  ];

  const analysisTooltips = [
    "Body Language and Facial Expressions analysis provides insights into the subject's non-verbal communication cues, such as facial expressions and body language.",
    "Speech and Language Analysis examines the subject's spoken language, including speech patterns, word choice, and fluency.",
    "Speech Tone analysis evaluates the emotional tone of the subject's speech, such as their level of enthusiasm, confidence, or stress.",
    "Attention Tracking analysis monitors the subject's visual attention and engagement with the presented content or stimuli.",
    "Audio Analysis assesses the quality and accuracy of the audio signals captured during the interaction.",
    "Answer Quality Analysis checks the structure and content of your answers for each question to generate a smart feedback",
  ];

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
      <Stepper
        activeStep={5}
        alternativeLabel
        sx={{
          "& .MuiStepIcon-root": {
            // Default state color
            fill: theme.palette.primary.main, // Default icon color
            "&$completed": {
              fill: theme.palette.primary.main, // Completed state color
            },
            "&$active": {
              color: theme.palette.primary.main, // Active state color
            },
          },
          "& .MuiStepIcon-completed": {
            color: theme.palette.primary.main, // Ensure completed uses primary color
          },
          "& .MuiStepIcon-active": {
            color: theme.palette.primary.main, // Ensure active uses primary color
          },
        }}
      >
        {steps.map((step) => (
          <Step key={step.label}>
            <StepLabel>{step.label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Grid container spacing={2} sx={{ padding: theme.spacing(3) }}>
        <Grid item xs={12} md={6}>
          <ReactPlayer
            url="https://dwi4xjqduw0ng.cloudfront.net/past-session-react.mp4"
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
          <Box
            sx={{
              maxHeight: 470,
              overflow: "auto",
              borderBottom: 1,
              borderColor: theme.palette.text.disabled,
            }}
          >
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
            {analysisData.map((analysis, index) => (
              <Tab label={analysis.tabTitle} />
            ))}
          </Tabs>
        </Box>
        <Box>
          {analysisData.map((analysis, index) => (
            <Box
              key={index}
              role="tabpanel"
              hidden={activeDetailsTab !== index}
              sx={{ flexGrow: 1, mt: 2 }}
            >
              <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                <Typography variant="h3" align="center">
                  {analysis.title}
                </Typography>
                <Tooltip title={analysisTooltips[index]} placement="top" arrow>
                  <IconButton aria-label="info" sx={{ ml: 1 }}>
                    <InfoOutlined sx={{ fill: "#1890FF" }} />
                  </IconButton>
                </Tooltip>
              </Box>
              {analysis.content}
            </Box>
          ))}
        </Box>
      </Box>
    </>
  );
}

export default SessionDetails;
