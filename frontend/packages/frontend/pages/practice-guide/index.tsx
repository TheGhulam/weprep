import React from "react";
import { Box, Grid, Typography, Button } from "@mui/material";
import PracticeGuide from "@/components/PracticeGuides/PracticeGuide";

const guides = [
    {
      "title": "Learn Star Method of Answering Questions",
      "youtubeLink": "https://www.youtube.com/watch?v=uQEuo7woEEk",
      "courseraLink": "https://www.coursera.org/projects/accomplishment-star-techniques-for-job-interviews",
      "articleLink": "https://www.themuse.com/advice/star-interview-method"
    },
    {
      "title": "Learn Spring Annotations",
      "youtubeLink": "https://www.youtube.com/watch?v=wf70Hs-aCcI",
      "courseraLink": "https://www.coursera.org/learn/spring-mvc-rest-controller",
      "articleLink": "https://www.javatpoint.com/spring-boot-annotations#:~:text=Spring%20Boot%20Annotations%20is%20a,of%20the%20code%20they%20annotate."
    },
    {
      "title": "Practice Word Pacing",
      "youtubeLink": "https://www.youtube.com/watch?v=PlJaaUYIwIM",
      "courseraLink": "https://www.coursera.org/specializations/good-with-words-speaking-and-presenting",
      "articleLink": "https://www.linkedin.com/advice/3/how-do-you-pace-your-speech-skills-public-speaking#:~:text=5%20Pacing%20tips,-To%20effectively%20pace&text=Listen%20to%20your%20voice%20and,%2C%20articulating%2C%20and%20replacing%20them."
    },
    {
      "title": "Practice Avoiding Filler Words",
      "youtubeLink": "https://www.youtube.com/watch?v=W995352_kkw",
      "courseraLink": "https://www.coursera.org/learn/finding-your-professional-voice",
      "articleLink": "https://www.storytellingwithdata.com/blog/avoid-filler-words"
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
   