import React, { useEffect, useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  IconButton,
  Avatar,
  Divider,
} from "@mui/material";
import VideoCameraFrontIcon from "@mui/icons-material/VideoCameraFront";
import MicIcon from "@mui/icons-material/Mic";
import MicOffIcon from "@mui/icons-material/MicOff";
import VideocamOutlinedIcon from "@mui/icons-material/VideocamOutlined";
import VideocamIcon from "@mui/icons-material/Videocam";
import VideocamOffIcon from "@mui/icons-material/VideocamOff";
import CancelIcon from "@mui/icons-material/Cancel";
import PlayCircleFilledIcon from "@mui/icons-material/PlayCircleFilled";
import Webcam from "react-webcam";
import { useRouter } from "next/router";
import { CheckCircle, StopCircle } from "@mui/icons-material";
import VolumeUpIcon from "@mui/icons-material/VolumeUp";

const videoConstraints = {
  //   width: { min: 480 },
  //   height: { min: 720 },
  //   aspectRatio: 0.6666666667,/
  facingMode: "user",
};

function VideoCall() {
  // State to manage camera and mic status
  const [cameraEnabled, setCameraEnabled] = React.useState(false);
  const [micEnabled, setMicEnabled] = React.useState(false);
  const router = useRouter();

  const onCancel = () => {
    router.push(`/dashboard`);
  };

  const onFinishSession = () => {
    router.push(`/live-practice-session/finished`);
  };
  const [timeElapsed, setTimeElapsed] = useState(0);
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? "0" : ""}${remainingSeconds}`;
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeElapsed((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <Box sx={{ height: "100vh", backgroundColor: "#0C090A", color: "white", padding: 2 }}>
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar>
          <IconButton disabled edge="start" color="inherit" aria-label="menu">
            <VideoCameraFrontIcon style={{ fill: "#fff" }} />
          </IconButton>
          <Typography variant="h6" sx={{ marginLeft: 1, color: "#FFF" }}>
            Sales Pitch
          </Typography>
          <Divider orientation="vertical" flexItem sx={{ mx: 2, backgroundColor: "grey", mr: 4 }} />
          <IconButton disabled edge="start" color="inherit" aria-label="menu">
            <VolumeUpIcon style={{ fill: "#fff" }} />
          </IconButton>
          <Typography variant="h6" sx={{ color: "#FFF" }}>
            Faaiz Khan | You
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
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" mt={8}>
        <Box
          sx={{
            // width: "100%",
            height: 700,
            backgroundColor: "#0F1115",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Webcam
            width={"100%"}
            height={"100%"}
            videoConstraints={videoConstraints}
            mirrored={true}
            audio={true}
          />
        </Box>
        <Box sx={{ mt: 4, display: "flex", gap: 2 }}>
          <Button
            size="large"
            variant="contained"
            color="primary"
            startIcon={<CheckCircle style={{ fill: "#fff" }} />}
            sx={{
              backgroundColor: "#12A150",
              "&:hover": {
                backgroundColor: "#007231",
              },
            }}
            onClick={onFinishSession}
          >
            Finish Session
          </Button>
        </Box>
      </Box>
    </Box>
  );
}

export default VideoCall;
