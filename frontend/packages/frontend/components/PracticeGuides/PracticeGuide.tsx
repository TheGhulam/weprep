import React, { useState } from "react";
import { Typography, Link, Grid, Stepper, Step, StepButton, Button } from "@mui/material";

interface Guide {
  title: string;
  youtubeLink: string;
  courseraLink: string;
  articleLink: string;
}

interface PracticeGuideProps {
  guides: Guide[];
}

const PracticeGuide: React.FC<PracticeGuideProps> = ({ guides }) => {
  const [activeStep, setActiveStep] = useState<number>(0);

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
        <Stepper activeStep={activeStep} alternativeLabel>
          {guides.map((guide, index) => (
            <Step key={index}>
              <StepButton onClick={handleStep(index)}>
                {guide.title}
              </StepButton>
            </Step>
          ))}
        </Stepper>
      </Grid>
      <Grid item xs={12} sm={4} sx={{ padding: 2 }}>
        <Link
          href={activeGuide.youtubeLink}
          target="_blank"
          rel="noopener noreferrer"
          variant="body1"
          color="primary"
          underline="hover"
        >
          YouTube Video
        </Link>
      </Grid>
      <Grid item xs={12} sm={4} sx={{ padding: 2 }}>
        <Link
          href={activeGuide.courseraLink}
          target="_blank"
          rel="noopener noreferrer"
          variant="body1"
          color="primary"
          underline="hover"
        >
          Coursera Course
        </Link>
      </Grid>
      <Grid item xs={12} sm={4} sx={{ padding: 2 }}>
        <Link
          href={activeGuide.articleLink}
          target="_blank"
          rel="noopener noreferrer"
          variant="body1"
          color="primary"
          underline="hover"
        >
          Web Article
        </Link>
      </Grid>
      <Grid item xs={12}>
        <Grid container justifyContent="center">
          <Button
            size="large"
            variant="contained"
            sx={{ textTransform: "none", height: "fit-content" }}
            onClick={handleNext}
            disabled={activeStep === guides.length - 1}
          >
            Next Step
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default PracticeGuide;
