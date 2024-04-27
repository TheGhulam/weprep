import React, { useState, useEffect, useRef } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  IconButton,
  Avatar,
  Divider,
  Card,
  Grid,
  CircularProgress,
} from "@mui/material";
import VideoCameraFrontIcon from "@mui/icons-material/VideoCameraFront";
import MicIcon from "@mui/icons-material/Mic";
import MicOffIcon from "@mui/icons-material/MicOff";
import VolumeUpIcon from "@mui/icons-material/VolumeUp";
import VideocamIcon from "@mui/icons-material/Videocam";
import VideocamOffIcon from "@mui/icons-material/VideocamOff";
import CancelIcon from "@mui/icons-material/Cancel";
import PlayCircleFilledIcon from "@mui/icons-material/PlayCircleFilled";
import Webcam from "react-webcam";
import { useRouter } from "next/router";
import ReplayIcon from "@mui/icons-material/Replay"; // Assuming 'repeat' icon means 'Replay'
import SkipNextIcon from "@mui/icons-material/SkipNext";
import ReactPlayer from "react-player";
import StopCircleIcon from "@mui/icons-material/StopCircle";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { red, grey } from "@mui/material/colors";

const questionsData = [
  {
    index: 1,
    text: "Hello Faaiz Khan, it's great to meet you. I'll be conducting your interview today for the Data Scientist position. We'll go through a series of questions, and you can answer each one after I finish asking it. Let's get started.",
    videoSrc: "https://dwi4xjqduw0ng.cloudfront.net/intro-b.mp4",
  },
  {
    index: 2,
    text: "Given the requirement to scrape data from a website that employs measures like rate limiting and IP blocking to prevent scraping, walk me through your approach to designing a resilient and efficient scraping solution.",
    videoSrc: "https://dwi4xjqduw0ng.cloudfront.net/question1-b.mp4",
  },
  {
    index: 3,
    text: "Imagine you're tasked with processing a large dataset containing a mix of text, images, and JSON data. Describe your strategy for cleaning, transforming, and structuring this data into a format suitable for machine learning tasks.",
    videoSrc: "https://dwi4xjqduw0ng.cloudfront.net/question3-b.mp4",
  },
  {
    index: 4,
    text: "Let's say you need to build a web application for our AI team to filter and moderate scraped data. Demonstrate how you would design the user interface and core functionalities to facilitate efficient data review and labeling.",
    videoSrc: "https://dwi4xjqduw0ng.cloudfront.net/question4-b.mp4",
  },
  {
    index: 5,
    text: "Explain the concept of object storage and its advantages compared to traditional relational databases, particularly in the context of storing and managing large volumes of unstructured data.",
    videoSrc: "https://dwi4xjqduw0ng.cloudfront.net/question5-b.mp4",
  },
  {
    index: 6,
    text: "Considering the rapidly evolving field of AI, how do you stay updated on the latest technologies and trends in data engineering and software development?",
    videoSrc: "https://dwi4xjqduw0ng.cloudfront.net/question6-new-b.mp4",
  },
];

const silentVideo = "https://dwi4xjqduw0ng.cloudfront.net/silence-b.mp4";

enum Speaker {
  AI = "AI",
  USER = "USER",
}

function VideoCall() {
  // State to manage camera and mic status
  const [currentSpeaker, setCurrentSpeaker] = useState(Speaker.AI);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(questionsData[0]);
  const [currentVideoUrl, setCurrentVideoUrl] = useState(currentQuestion.videoSrc);
  const playerRef = useRef(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeElapsed((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? "0" : ""}${remainingSeconds}`;
  };
  const router = useRouter();

  const toggleSpeaker = () => {
    if (currentSpeaker === Speaker.AI) {
      setCurrentSpeaker(Speaker.USER);
    } else {
      setCurrentSpeaker(Speaker.AI);
    }
  };

  const playNext = () => {
    if (playerRef.current) {
      (playerRef.current as any).seekTo(0, "seconds");
      ((playerRef.current as any).getInternalPlayer() as HTMLVideoElement).play();
    }
  };

  const onSkip = () => {
    if (questionsData.length > currentQuestion.index) {
      setCurrentQuestion(questionsData[currentQuestion.index]);
      setCurrentVideoUrl(questionsData[currentQuestion.index].videoSrc);
      playNext();
    } else {
      onEndSession();
    }
  };
  const onRepeat = () => {
    setCurrentSpeaker(Speaker.AI);
    setCurrentVideoUrl(currentQuestion.videoSrc);
    if (playerRef.current) {
      (playerRef.current as any).seekTo(0, "seconds");
      ((playerRef.current as any).getInternalPlayer() as HTMLVideoElement).play();
    }
  };

  const onEndSession = () => {
    router.push(`/live-practice-session/finished`);
  };

  const onFinishAnswer = () => {
    toggleSpeaker();
    if (questionsData.length > currentQuestion.index) {
      setCurrentQuestion(questionsData[currentQuestion.index]);
      onSkip();
    } else {
      onEndSession();
    }
  };

  const handleVideoEnd = () => {
    console.log("Video ended");
    if (currentVideoUrl === silentVideo) {
      if (playerRef.current) {
        (playerRef.current as any).seekTo(0, "seconds");
        ((playerRef.current as any).getInternalPlayer() as HTMLVideoElement).play();
      }
      return;
    } else if (currentQuestion === questionsData[0]) {
      onSkip();
      return;
    }
    setCurrentVideoUrl(silentVideo);
    toggleSpeaker(); // Replay the video automatically or handle as needed
  };

  return (
    <Box sx={{ height: "100vh", backgroundColor: "#0C090A", color: "white", padding: 2 }}>
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar>
          <IconButton disabled edge="start" color="inherit" aria-label="menu">
            <VideoCameraFrontIcon style={{ fill: "#fff" }} />
          </IconButton>
          <Typography variant="h6" sx={{ marginLeft: 1, color: "#FFF" }}>
            Mock Interview
          </Typography>
          <Divider orientation="vertical" flexItem sx={{ mx: 2, backgroundColor: "grey", mr: 4 }} />
          <IconButton disabled edge="start" color="inherit" aria-label="menu">
            <VolumeUpIcon style={{ fill: "#fff" }} />
          </IconButton>
          <Typography variant="h6" sx={{ color: "#FFF" }}>
            {currentSpeaker === Speaker.AI ? "Jane Sandberg  | AI Interviewer" : "Faaiz Khan | You"}
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "flex-end" }}>
            <Typography variant="h6" sx={{ color: "#FFF" }}>
              Live
            </Typography>
            <Typography variant="body2" sx={{ color: "#FFF" }}>
              {formatTime(timeElapsed)}
            </Typography>
          </Box>
          <Box
            sx={{
              width: 10,
              height: 10,
              backgroundColor: "red",
              borderRadius: "50%",
              animation: "blink 1s infinite",
              marginLeft: 2,
            }}
          />
        </Toolbar>
      </AppBar>
      <Divider />
      <Grid container spacing={2} sx={{ height: "100vh", padding: 2 }}>
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            height: "75%",
          }}
        >
          <Webcam
            // audio={true}
            mirrored={true}
            videoConstraints={{ width: 1280, height: 720, facingMode: "user" }}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              borderRadius: "15px",
            }}
          />
        </Grid>
        <Grid item xs={12} md={6} sx={{ height: "75%" }}>
          {" "}
          <Box
            sx={{
              width: "100%",
              height: "70%",
              marginBottom: 0.5,
              border: currentSpeaker == Speaker.AI ? 1 : 0,
              borderColor: "#E2F1FA",
              borderRadius: 1,
            }}
          >
            <ReactPlayer
              ref={playerRef}
              width="100%"
              height="100%"
              style={{ objectFit: "cover", borderRadius: "15px" }}
              url={currentVideoUrl}
              playing={true}
              controls={false}
              onEnded={handleVideoEnd}
            />
          </Box>
          <Card
            sx={{
              height: "30%",
              backgroundColor: "#FFF",
              color: "#00255A",
              padding: 2,
              borderRadius: "10px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <Typography variant="h6" gutterBottom>
              {currentQuestion.index === 1
                ? "Introduction"
                : `Question ${currentQuestion.index - 1}`}
            </Typography>
            <Typography variant="subtitle1">{currentQuestion.text}</Typography>
            <Box
              sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mt: 1 }}
            >
              <Button
                size="large"
                variant="contained"
                disabled={currentSpeaker == Speaker.AI || currentQuestion.index === 1}
                sx={{
                  mr: 2,
                  backgroundColor: "#2A93D5",
                  "&:hover": {
                    backgroundColor: "#00255A",
                  },
                  "&:disabled": {
                    backgroundColor: grey[200],
                    color: grey[500],
                  },
                }}
                startIcon={<CheckCircleIcon style={{ fill: "#FFF" }} />}
                onClick={onFinishAnswer}
              >
                Finished Answering
              </Button>

              <Box sx={{ display: "flex" }}>
                <Button
                  variant="contained"
                  onClick={onRepeat}
                  startIcon={<ReplayIcon sx={{ fill: "#fff" }} />}
                >
                  Repeat
                </Button>
                <Button
                  variant="contained"
                  startIcon={<SkipNextIcon sx={{ fill: "#fff" }} />}
                  onClick={onSkip}
                  sx={{ ml: 1 }}
                >
                  Skip
                </Button>
              </Box>
            </Box>
          </Card>
        </Grid>
      </Grid>
      <AppBar
        color="transparent"
        position="fixed"
        sx={{
          top: "auto",
          bottom: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          p: 1,
        }}
      >
        <Button
          size="large"
          variant="contained"
          startIcon={<StopCircleIcon sx={{ mr: 3, fill: "#fff" }} />}
          onClick={onEndSession}
          sx={{
            width: "15rem",
            backgroundColor: "#CC525F", // Custom red color for the button
            color: "#FFF", // Text color is white
            "&:hover": {
              backgroundColor: "#E06370", // Lighter red on hover
            },
            marginBottom: 4, // Margin from the bottom of the AppBar
          }}
        >
          End Session
        </Button>
      </AppBar>
    </Box>
  );
}

export default VideoCall;
