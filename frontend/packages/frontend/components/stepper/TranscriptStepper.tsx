import React from "react";
import { Typography, Stepper, Step, StepLabel, StepContent, Box, useTheme } from "@mui/material";

function TranscriptStepper() {
  const theme = useTheme();
  const questions = [
    {
      question:
        "Could you share your experience with unit testing in React applications? Specifically, how do you approach writing unit tests and which tools do you find most effective?",
      answer:
        "Yes, I have extensive experience with unit testing in React. I use tools like Jest and React Testing Library to write unit tests for components and utility functions. I follow best practices such as mocking dependencies and testing edge cases to ensure robust test coverage.",
    },
    {
      question:
        "In your experience, how do you manage state in large-scale React projects? What tools and strategies do you rely on to handle complex state management effectively?",
      answer:
        "In large-scale React applications, I prefer using state management libraries like Redux or MobX to manage complex application states. These libraries provide centralized state management, making it easier to maintain and scale the application. I also utilize features like middleware and selectors to optimize performance and maintainability.",
    },
    {
      question:
        "What techniques do you use to optimize the performance of React applications? Can you discuss some specific strategies that have proven effective in your past projects?",
      answer:
        "To optimize the performance of React applications, I employ various strategies such as code splitting to reduce initial bundle size, memoization to prevent unnecessary re-renders, and implementing virtualized lists for efficient rendering of large datasets. I also leverage browser dev tools like Chrome DevTools and React Developer Tools to identify performance bottlenecks and make data-driven optimizations.",
    },
    {
      question:
        "Accessibility is critical in web development. How do you ensure your React applications are accessible? Could you describe some practices you implement to enhance accessibility?",
      answer:
        "Ensuring accessibility in React applications is crucial. I follow accessibility best practices by using semantic HTML elements, providing alternative text for images, and ensuring keyboard navigation and screen reader compatibility. I also utilize ARIA attributes and run accessibility audits using tools like Axe to identify and address accessibility issues.",
    },
    {
      question:
        "Can you explain how you incorporate React hooks into your projects? What are some of the benefits you've found in using hooks, especially compared to traditional class components?",
      answer:
        "React hooks are functions that enable functional components to use state and lifecycle features without writing a class. I extensively use hooks like useState for managing component state, useEffect for handling side effects, and custom hooks for code reuse and abstraction. Hooks allow me to write cleaner and more concise code compared to class components.",
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
          },
        }}
      >
        {questions.map((item, index) => (
          <Step key={index} expanded>
            <StepLabel>{item.question}</StepLabel>
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
