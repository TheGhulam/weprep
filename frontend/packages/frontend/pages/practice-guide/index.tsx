import React from "react";
import { Box, Grid, Typography, Button } from "@mui/material";
import PracticeGuide from "@/components/PracticeGuides/PracticeGuide";

const guides = [
    {
      "title": "Learn Star Method of Answering Questions",
      "youtubeLink": "https://www.youtube.com/watch?v=hdI2bqOjy3c",
      "courseraLink": "https://www.coursera.org/learn/javascript",
      "articleLink": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"
    },
    {
      "title": "Learn Spring Annotations",
      "youtubeLink": "https://www.youtube.com/watch?v=Ke90Tje7VS0",
      "courseraLink": "https://www.coursera.org/learn/react",
      "articleLink": "https://reactjs.org/docs/getting-started.html"
    },
    {
      "title": "Practice Word Pacing",
      "youtubeLink": "https://www.youtube.com/watch?v=hdI2bqOjy3c",
      "courseraLink": "https://www.coursera.org/learn/javascript",
      "articleLink": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"
    },
    {
      "title": "Practice Avoiding Filler Words",
      "youtubeLink": "https://www.youtube.com/watch?v=Ke90Tje7VS0",
      "courseraLink": "https://www.coursera.org/learn/react",
      "articleLink": "https://reactjs.org/docs/getting-started.html"
    }
  ]

export default function AnalyticsPage() {
    return (
        <>
            <Typography variant="h2" align="center" gutterBottom>
                Practice Guide
            </Typography>
            <PracticeGuide guides={guides}/>
        </>
    );
}
   