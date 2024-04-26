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

const exampleUrl =
  "https://ai-interview-stub-video.s3.us-east-1.amazonaws.com/placeholder-ai-video.mp4?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGMaCXVzLWVhc3QtMSJIMEYCIQDlthtQfLMR40uCzj6QjxCOquIBMemdUTWf5I2df7r0KwIhAPPE6XzTyZIEahX2HhbLohzapX44vvoSjZl3VgUlPB6FKu0CCKz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNTMzMjY3Mzc5NDQ0IgxOLW2UPvJUPLrpuqkqwQJT0MycjxBEV85TaJAHqBHVRnE938pIQTWTCDi0GOpFxzC1AziIRVaySQMlGQeliqlYX0Wv4Q%2FxZkN3Ut3710xrMb0Yyf0R8kOahp%2F2X3zNlOWE%2Bc%2BVq6%2FVvqZz2AYi%2B6CKM9zsjRrtRp8rl%2BArVBabUEPVFr%2FkXyNz2Y%2BYbsFZNMC66jaKuNfD%2BNP8jrWqoIldLEBJDPsigDTYSmLC5Wx5TwrZte8GmeyTeOBI7BZSobeU9LIP%2BBJOPzN2jbDteKeir%2F%2FU4K%2F3sN2QW6Z1lQXpfJa%2BnxVOMdkyC6NirDbj0LuStRfwRr%2FaSQbMBw010VGflIqOaHPzd1JClFc9I%2BgTmPW%2BYmuiT2cLRc80XuybKSmpKTWULeR6s%2FKZ0iNnl8h6sQGxdXQ%2BXWE0urUtQ50PQ%2Fm4O8%2FxBIehgR5A5fgr1Pcwpc2qsQY6sgJAzHpoUMDqXg5pY%2BtakTHQVauZ%2FUV1gWNmzEvxfQ5Ccq3UYoKKBXIdEZt3DRwog8BxjG1Fxqbw7FOleA4bzZJQrCJOojbZFzffhFqnmk8IUpZYXoT9RikJmYV%2FZDZoDSE%2BfCaHrW0o2HkLL2rokY5YcXDDN2ILrecOmyg4Toov2k1yuTP6FrgwZ6gHVfkbsoGQuUJ24TXRQpcuYlyyZ2PsOXqT%2BfhrXITPBYAAC8oxDiXcnq3%2FXftAscLjjCl3l0EP9jiPuzu3OlOCbZzk4iSz%2FjrIb9Pw6od%2FUAStIRK5C6RmlCeN5%2BriIw%2BupYiksHPFHLo6YyRr1eM7JuOKXe8vFOIzH5U01EFLIC%2BG0Z606a%2F9dcfss54L6%2FpjSrztzfx2oc%2BsyrJHY57ji6OnvdcJBs4%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240425T190518Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAXYKJWOT2HPYL4TMZ%2F20240425%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=1c5556e2e80349b98f597e5edd8470f33ffa43e9a0cae4262a6b394ff1f77d30";

const questionsData = [
  {
    index: 1,
    text: "Given the requirement to scrape data from a website that employs measures like rate limiting and IP blocking to prevent scraping, walk me through your approach to designing a resilient and efficient scraping solution.",
  },
  {
    index: 2,
    text: "Imagine you're tasked with processing a large dataset containing a mix of text, images, and JSON data. Describe your strategy for cleaning, transforming, and structuring this data into a format suitable for machine learning tasks.",
  },
  {
    index: 3,
    text: "Let's say you need to build a web application for our AI team to filter and moderate scraped data. Demonstrate how you would design the user interface and core functionalities to facilitate efficient data review and labeling.",
  },
  {
    index: 4,
    text: "Explain the concept of object storage and its advantages compared to traditional relational databases, particularly in the context of storing and managing large volumes of unstructured data.",
  },
  {
    index: 5,
    text: "Considering the rapidly evolving field of AI, how do you stay updated on the latest technologies and trends in data engineering and software development?",
  },
];

enum Speaker {
  AI = "AI",
  USER = "USER",
}

function VideoCall() {
  // State to manage camera and mic status
  const [currentSpeaker, setCurrentSpeaker] = useState(Speaker.AI);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(questionsData[0]);
  const [currentVideoUrl, setCurrentVideoUrl] = useState(exampleUrl);
  const playerRef = useRef(null);

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
      playNext();
    }
  };
  const onRepeat = () => {
    setCurrentSpeaker(Speaker.AI);
    if (playerRef.current) {
      (playerRef.current as any).seekTo(0, "seconds");
      ((playerRef.current as any).getInternalPlayer() as HTMLVideoElement).play();
    }
  };
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

  const onEndSession = () => {
    router.push(`/live-practice-session/finished`);
  };

  const onFinishAnswer = () => {
    toggleSpeaker();
    playNext();
  };

  const handleVideoEnd = () => {
    console.log("Video ended");
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
            {currentSpeaker === Speaker.AI ? "Joy Banks | AI Interviewer" : "Faaiz Khan | You"}
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
              Question {currentQuestion.index}
            </Typography>
            <Typography variant="subtitle1">{currentQuestion.text}</Typography>
            <Box
              sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mt: 1 }}
            >
              <Button
                size="large"
                variant="contained"
                disabled={currentSpeaker == Speaker.AI}
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
