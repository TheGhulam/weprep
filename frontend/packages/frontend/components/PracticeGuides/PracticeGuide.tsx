import React, { useState } from "react";
import { Typography, Link, Grid, Stepper, Step, StepButton, Button, useTheme } from "@mui/material";
import ReactPlayer from "react-player";
import { CheckCircle } from "@mui/icons-material";

interface Guide {
  title: string;
  ytLink1: string;
  ytLink2: string;
  ytLink3: string;
}

interface PracticeGuideProps {
  guides: Guide[];
}

const PracticeGuide: React.FC<PracticeGuideProps> = ({ guides }) => {
  const [activeStep, setActiveStep] = useState<number>(0);
  const theme = useTheme();

  const handleStep = (step: number) => () => {
    setActiveStep(step);
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const activeGuide = guides[activeStep];

  return (
    <Grid container spacing={3} alignItems="center">
      <Grid item xs={12}>
        <Stepper
          activeStep={activeStep}
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
          {guides.map((guide, index) => (
            <Step key={index}>
              <StepButton onClick={handleStep(index)}>{guide.title}</StepButton>
            </Step>
          ))}
        </Stepper>
      </Grid>
      <Grid item xs={12} sm={4} sx={{ padding: 6, height: "40vh" }}>
        <ReactPlayer url={activeGuide.ytLink1} controls={true} width="100%" height="100%" />
      </Grid>
      <Grid item xs={12} sm={4} sx={{ padding: 6, height: "40vh" }}>
        <ReactPlayer url={activeGuide.ytLink2} controls={true} width="100%" height="100%" />
      </Grid>
      <Grid item xs={12} sm={4} sx={{ padding: 6, height: "40vh" }}>
        <ReactPlayer url={activeGuide.ytLink3} controls={true} width="100%" height="100%" />
      </Grid>
      <Grid item xs={12}>
        <Grid container justifyContent="center">
          <Button
            size="large"
            variant="contained"
            sx={{ textTransform: "none", height: "fit-content" }}
            onClick={handleNext}
            disabled={activeStep === guides.length - 1}
            startIcon={<CheckCircle sx={{ fill: "#fff" }} />}
          >
            Mark as Completed
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default PracticeGuide;
