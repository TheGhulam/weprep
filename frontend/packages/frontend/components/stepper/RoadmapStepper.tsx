import React from "react";
import {
  Typography,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Box,
  useTheme,
  Link,
} from "@mui/material";
import { IconCross } from "@tabler/icons-react";
import {
  ChecklistRtl,
  CircleNotifications,
  Lightbulb,
  LightbulbCircle,
  School,
} from "@mui/icons-material";
import StepIcon from "../atoms/StepIcon";

function FeedbackStepper() {
  const theme = useTheme();
  const recommendations = [
    {
      title: "Learn Start Method of Answering Questions",
      reason:
        "Learning the Start Method of Answering Questions will help you structure your responses more effectively at the beginning of interviews. This method guides you on how to clearly and concisely introduce your answers, making a strong first impression and setting the right tone for detailed discussions.",
      url: "https://www.youtube.com/watch?v=uQEuo7woEEk",
    },
    {
      title: "Advanced State Management with Redux",
      reason:
        "This resource dives deep into Redux and advanced state management techniques for large-scale React applications. It covers topics such as middleware, selectors, and best practices for organizing complex application states. Enhancing your understanding of these areas will improve your ability to handle state management in complex projects more efficiently.",
      url: "https://www.youtube.com/watch?v=rtwZrbpsbIY",
    },
    {
      title: "Effective Unit Testing in react",
      reason:
        "Studying Effective Unit Testing in React will provide you with a deeper understanding of how to create robust unit tests for your applications. You'll learn advanced techniques for using Jest and React Testing Library effectively, including mocking dependencies and testing edge cases, which are crucial for ensuring comprehensive test coverage.",
      url: "https://www.youtube.com/watch?v=OVNjsIto9xM",
    },
    {
      title: "Practice Word Pacing",
      reason:
        "Practicing word pacing is essential for improving the clarity and effectiveness of your spoken responses during interviews. This skill helps in pacing your delivery to make your answers more understandable and engaging, which is crucial for communicating complex ideas clearly.",
      url: "https://www.youtube.com/watch?v=032Hum9KNjw",
    },
  ];
  return (
    <Box mt={2}>
      <Stepper
        orientation="vertical"
        nonLinear
        sx={{
          "& .MuiStepIcon-root": {
            color: theme.palette.text.primary,
            "&.Mui-completed": {
              color: theme.palette.text.primary,
            },
            "&.Mui-active": {
              color: theme.palette.text.primary,
            },
            "& text": {
              fill: theme.palette.common.white,
            },
          },
          "& .MuiStepLabel-label": {
            color: theme.palette.text.primary,
            fontWeight: "700",
          },
        }}
      >
        {recommendations.map((item, index) => (
          <Step key={index} expanded>
            <StepLabel icon={<StepIcon index={index} />}>{item.title} </StepLabel>

            <StepContent>
              <Typography variant="body1">
                {item.reason}{" "}
                <Link href={item.url} target="_blank" rel="noopener noreferrer">
                  Checkout resources
                </Link>
              </Typography>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
}

export default FeedbackStepper;
