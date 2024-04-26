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

function FeedbackStepper() {
  const theme = useTheme();
  const recommendations = [
    {
      title: "Effective Unit Testing in React",
      reason:
        "This resource covers advanced techniques for unit testing in React applications, including using Jest and React Testing Library effectively, mocking dependencies, and testing edge cases. It will help the candidate further improve their unit testing skills and ensure robust test coverage.",
      url: "https://medium.com",
    },
    {
      title: "Advanced State Management with Redux",
      reason:
        "This resource dives deep into Redux and advanced state management techniques for large-scale React applications. It covers topics such as middleware, selectors, and best practices for organizing complex application states. It will enhance the candidate's understanding of state management in complex projects.",
      url: "https://medium.com",
    },
    {
      title: "React Performance Optimization Masterclass",
      reason:
        "This masterclass provides comprehensive guidance on optimizing React application performance. It includes in-depth discussions on code splitting, memoization, virtualization, and performance analysis using browser dev tools. It will equip the candidate with advanced techniques to optimize the performance of their React applications.",
      url: "https://medium.com",
    },
    {
      title: "Web Accessibility Best Practices for React Developers",
      reason:
        "This resource offers practical guidance on implementing accessibility best practices in React applications. It covers topics such as using semantic HTML, providing alternative text for images, and ensuring keyboard navigation and screen reader compatibility. It will help the candidate ensure their React applications are accessible to all users.",
      url: "https://medium.com",
    },
  ];
  return (
    <Box mt={2}>
      <Typography variant="body1" mb={2} mr={2} ml={2}>
        To improve, the candidate should research and learn more about STAR answering structure.
        They should also practice articulating their experiences and understanding of these
        methodologies
      </Typography>
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
          },
        }}
      >
        {recommendations.map((item, index) => (
          <Step key={index} expanded>
            <StepLabel>{item.title} </StepLabel>
            <StepContent>
              <Typography variant="body1">
                {item.reason}{" "}
                <Link ml={1} href={item.url} target="_blank" rel="noopener noreferrer">
                  Click to learn more
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
