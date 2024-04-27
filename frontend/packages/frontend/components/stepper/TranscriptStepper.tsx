import React from "react";
import { Typography, Stepper, Step, StepLabel, StepContent, Box, useTheme } from "@mui/material";
import StepIcon from "../atoms/StepIcon";

function TranscriptStepper() {
  const theme = useTheme();
  const questions = [
    {
      question:
        "Could you share your experience with unit testing in React applications? Specifically, how do you approach writing unit tests and which tools do you find most effective?",
      answer:
        "Oh, yes, I have quite a bit of experience with unit testing in React. Umm, I typically use tools like Jest and the React Testing Library to, you know, write unit tests for both components and utility functions. I really focus on following best practices, like mocking dependencies and testing those tricky edge cases, to make sure we have solid test coverage.",
    },
    {
      question:
        "In your experience, how do you manage state in large-scale React projects? What tools and strategies do you rely on to handle complex state management effectively?",
      answer:
        "In large-scale React projects, I usually lean towards using, um, state management libraries like Redux or MobX. These tools provide centralized state management which really helps in maintaining and scaling the application. I also like to use features like middleware and selectors to, you know, optimize performance and enhance maintainability.",
    },
    {
      question:
        "What techniques do you use to optimize the performance of React applications? Can you discuss some specific strategies that have proven effective in your past projects?",
      answer:
        "To boost the performance of React applications, I apply a variety of strategies. Code splitting is a big one to cut down the initial bundle size, and I also use memoization to avoid unnecessary re-renders. Oh, and implementing virtualized lists is key for efficiently rendering large datasets. I frequently use browser dev tools, like Chrome DevTools and React Developer Tools, to spot performance bottlenecks and, like, make optimizations based on actual data.",
    },
    {
      question:
        "Accessibility is critical in web development. How do you ensure your React applications are accessible? Could you describe some practices you implement to enhance accessibility?",
      answer:
        "Accessibility, right, that's crucial. I ensure that my React applications are accessible by, um, sticking to accessibility best practices. This means using semantic HTML elements, providing alternative text for images, and making sure everything works with keyboard navigation and screen readers. I also use ARIA attributes and run accessibility audits with tools like Axe to find and fix any accessibility issues.",
    },
    {
      question:
        "Can you explain how you incorporate React hooks into your projects? What are some of the benefits you've found in using hooks, especially compared to traditional class components?",
      answer:
        "So, React hooks are these functions that let you use state and lifecycle features without needing to write a class. I use them a lot—like useState for managing component state, useEffect for handling side effects, and custom hooks for, you know, reusing code and creating abstractions. Hooks really help me write cleaner and more concise code, especially compared to traditional class components.",
    },
  ];

  return (
    <Box mt={2}>
      <Stepper
        orientation="vertical"
        nonLinear
        sx={{
          "& .MuiStepIcon-root": {
            // Style the step icons
            color: theme.palette.primary.main, // Icon color for all states
            "& text": {
              // Text inside the icon
              fill: theme.palette.common.white, // Making the text white
            },
          },
          "& .MuiStepLabel-label": {
            // Label styling
            color: theme.palette.text.primary, // Text color for the labels
            fontWeight: "600",
          },
        }}
      >
        {questions.map((item, index) => (
          <Step key={index} expanded>
            <StepLabel icon={<StepIcon index={index}></StepIcon>}>{item.question}</StepLabel>
            <StepContent>
              <Typography>{item.answer}</Typography>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
}

export default TranscriptStepper;
