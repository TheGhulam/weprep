import React from "react";
import { Box, Typography, useTheme } from "@mui/material";

const StepIcon = ({ index }) => {
  const theme = useTheme();
  return (
    <Box
      sx={{
        width: 30,
        height: 30,
        backgroundColor: theme.palette.primary.main, // Use primary color from theme
        color: "#FFF", // White color for the text
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        borderRadius: "50%", // Make the box circular
      }}
    >
      <Typography variant="subtitle2" component="div" sx={{ color: "#fff" }}>
        {index + 1}
      </Typography>
    </Box>
  );
};

export default StepIcon;
