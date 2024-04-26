import React from "react";
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Typography,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  useTheme,
  Tooltip,
  Divider,
} from "@mui/material";

function FeedbackStepper() {
  const theme = useTheme();
  const questionsWithFeedback = [
    {
      question: "Can you describe your experience with unit testing in React applications?",
      feedback:
        "The candidate demonstrated a strong understanding of unit testing in React applications. Their explanation of tools like Jest and React Testing Library was clear and thorough. They emphasized the importance of robust test coverage and best practices such as mocking dependencies and testing edge cases.",
      correctness_score: 8,
      structure_score: 8,
      detail_score: 8,
      preciseness_score: 7,
      relevancy_score: 9,
      comment:
        "The candidate effectively described a specific problem and provided clear solutions, demonstrating a good understanding of both front-end and back-end challenges.",
      suggestion:
        "Including metrics or specific outcomes beyond the 20% server load reduction would enhance the preciseness and impact of the response.",
    },
    {
      question: "How do you handle state management in large-scale React applications?",
      feedback:
        "The candidate provided a comprehensive overview of state management in large-scale React applications. Their preference for state management libraries like Redux or MobX showcased their understanding of managing complex application states. They highlighted features like middleware and selectors to optimize performance and maintainability.",
      correctness_score: 7,
      structure_score: 7,
      detail_score: 6,
      preciseness_score: 6,
      relevancy_score: 7,
      comment:
        "The answer gives a general idea of the problem and solution but lacks the specific details and technical depth found in the first response.",
      suggestion:
        "Adding more specific details about the technical challenges and the solutions applied would make the answer more compelling.",
    },
    {
      question:
        "What strategies do you employ for optimizing the performance of React applications?",
      feedback:
        "The candidate demonstrated expertise in optimizing React application performance. Their discussion of strategies such as code splitting, memoization, and virtualized lists showed a deep understanding of performance optimization techniques. They also mentioned using browser dev tools for performance analysis.",
      correctness_score: 3,
      structure_score: 4,
      detail_score: 2,
      preciseness_score: 2,
      relevancy_score: 3,
      comment:
        "The response is vague and lacks both technical details and a clear description of the problem and solution, indicating limited understanding or engagement with the topic.",
      suggestion:
        "Focus on providing a clear, detailed example with specific technical elements to demonstrate competence and experience in handling such issues.",
    },
    {
      question: "How do you ensure accessibility in your React applications?",
      feedback:
        "The candidate exhibited a strong commitment to accessibility in React applications. Their explanation of using semantic HTML elements, providing alternative text for images, and ensuring keyboard navigation and screen reader compatibility demonstrated thorough knowledge of accessibility best practices.",
      correctness_score: 8,
      structure_score: 9,
      detail_score: 9,
      preciseness_score: 8,
      relevancy_score: 9,
      comment:
        "The response was well-rounded, addressing various aspects of accessibility with practical examples.",
      suggestion:
        "Consider discussing global accessibility standards and certifications to further enhance the response.",
    },
    {
      question: "Can you explain the concept of React hooks and how you use them in your projects?",
      feedback:
        "The candidate provided a clear explanation of React hooks and their usage in functional components. Their discussion of useState, useEffect, and custom hooks showcased practical experience with hooks. Their preference for hooks over class components indicates familiarity with modern React patterns.",
      correctness_score: 8,
      structure_score: 8,
      detail_score: 8,
      preciseness_score: 7,
      relevancy_score: 9,
      comment:
        "Excellent use of examples to illustrate the use of hooks, enhancing understanding of their practical applications.",
      suggestion:
        "Explore the challenges encountered while using hooks and how they were overcome to provide a more comprehensive view.",
    },
    {
      question:
        "How do you approach code organization and project structure in React applications?",
      feedback:
        "The candidate demonstrated strong organizational skills in React application development. Their explanation of modular and scalable project structures, feature-based folder structures, and tooling for code formatting showcased a disciplined approach to code organization. Their adherence to coding conventions ensures consistency across the codebase.",
      correctness_score: 9,
      structure_score: 9,
      detail_score: 8,
      preciseness_score: 8,
      relevancy_score: 9,
      comment:
        "The candidate provides an effective overview of modern best practices in project organization for React.",
      suggestion:
        "Discussing how these practices integrate with continuous integration/continuous deployment (CI/CD) pipelines could provide additional insights into their development workflow.",
    },
  ];
  const scoreLabel = (label, value, description) => (
    <Tooltip title={description} placement="right" arrow>
      <Box sx={{ display: "flex", alignItems: "center", width: "100%" }}>
        <Box sx={{ minWidth: 100 }}>
          <Typography variant="body2" color="text.secondary">
            {label}
          </Typography>
        </Box>
        <Box sx={{ width: "100%", mr: 1 }}>
          <LinearProgress variant="determinate" value={value * 10} />
        </Box>
        <Box sx={{ minWidth: 35 }}>
          <Typography variant="body2" color="text.secondary">{`${value}/10`}</Typography>
        </Box>
      </Box>
    </Tooltip>
  );
  return (
    <Box mt={2}>
      <Stepper
        orientation="vertical"
        nonLinear
        sx={{
          "& .Mui-disabled": {
            color: theme.palette.text.primary, // Customize disabled text color here
          },
        }}
      >
        {questionsWithFeedback.map((item, index) => (
          <Step key={index} expanded>
            <StepLabel>{item.question}</StepLabel>
            <StepContent>
              {/* <Typography paragraph>{item.feedback}</Typography> */}
              <List dense sx={{ mr: 4 }}>
                {scoreLabel(
                  "Correctness",
                  item.correctness_score,
                  "Measures how accurate the response is to the question asked."
                )}
                {scoreLabel(
                  "Structure",
                  item.structure_score,
                  "Evaluates the logical organization and clarity of the response."
                )}
                {scoreLabel(
                  "Detail",
                  item.detail_score,
                  "Assesses the depth of detail and examples provided in the response."
                )}
                {scoreLabel(
                  "Preciseness",
                  item.preciseness_score,
                  "Rates the specificity and directness of the response to the question."
                )}
                {scoreLabel(
                  "Relevancy",
                  item.relevancy_score,
                  "Judges how relevant and on-topic the response is."
                )}
              </List>
              <Typography variant="body1">
                <span style={{ color: theme.palette.text.primary, textDecoration: "underline" }}>
                  Comment:
                </span>{" "}
                {item.comment}
              </Typography>
              <Typography variant="body1" mt={1}>
                <span style={{ color: theme.palette.text.primary, textDecoration: "underline" }}>
                  Suggestion:
                </span>{" "}
                {item.suggestion}
              </Typography>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
}

export default FeedbackStepper;
