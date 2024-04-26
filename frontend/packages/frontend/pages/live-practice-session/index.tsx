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
import { Pending } from "@mui/icons-material";
import { SessionType } from "@/Enums/SessionType";

const videoConstraints = {
  facingMode: "user",
};

function VideoCall() {
  // State to manage camera and mic status
  const [cameraEnabled, setCameraEnabled] = React.useState(false);
  const [micEnabled, setMicEnabled] = React.useState(false);
  const router = useRouter();
  const [sessionType, setSessionType] = React.useState<SessionType | undefined>();

  useEffect(() => {
    if (router.isReady) {
      const type = decodeURIComponent(router.query.sessionType as string);

      // Ensure the type from the query is a valid sessionType enum value
      if (type && Object.values(SessionType).includes(type)) {
        setSessionType(type as SessionType);
      }
    }
  }, [router.isReady, router.query]);

  const onCancel = () => {
    router.push(`/dashboard`);
  };

  const onJoinSession = () => {
    if (sessionType == SessionType.MockInterview) {
      router.push(`/live-practice-session/start-mock-interview`);
    } else if (sessionType == SessionType.PresentationPractice) {
      router.push(`/live-practice-session/start-presentation`);
    } else {
      router.push(`/live-practice-session/start-sales-pitch`);
    }
  };

  return (
    <Box sx={{ height: "100vh", backgroundColor: "#0C090A", color: "white", padding: 2 }}>
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
            <Pending style={{ fill: "#fff" }} />
          </IconButton>
          <Typography variant="h6" sx={{ marginLeft: 1, color: "#FFF" }}>
            Starting Session
          </Typography>
        </Toolbar>
      </AppBar>
      <Divider />
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" mt={8}>
        <Typography variant="h2" sx={{ color: "#FFF" }}>
          Get Started
        </Typography>
        <Typography variant="subtitle1" sx={{ color: "#A1A1AA", mb: 1 }}>
          Setup your audio and video before joining
        </Typography>
        <Box
          sx={{
            width: 630,
            height: 470,
            backgroundColor: "#0F1115",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {cameraEnabled ? (
            <>
              <Webcam
                width={"100%"}
                height={"100%"}
                videoConstraints={videoConstraints}
                mirrored={true}
                audio={true}
              />
            </>
          ) : (
            <>
              <Avatar
                src={"/user-avatar.svg"}
                sx={{
                  width: 200,
                  height: 200,
                }}
              />
              <Typography variant="h3" sx={{ mt: 1, color: "#FFF" }}>
                Faaiz Khan
              </Typography>
            </>
          )}
        </Box>
        <Box sx={{ marginTop: 2 }}>
          <IconButton
            onClick={() => setMicEnabled(!micEnabled)}
            sx={{
              backgroundColor: micEnabled ? "#000" : "#58585C",
              ":hover": {
                backgroundColor: "#343434",
              },
            }}
          >
            {micEnabled ? (
              <MicIcon style={{ fill: "#fff" }} />
            ) : (
              <MicOffIcon style={{ fill: "#fff" }} />
            )}
          </IconButton>
          <IconButton
            onClick={() => setCameraEnabled(!cameraEnabled)}
            sx={{
              ml: 1,
              backgroundColor: cameraEnabled ? "#000" : "#58585C",
              ":hover": {
                backgroundColor: "#343434",
              },
            }}
          >
            {cameraEnabled ? (
              <VideocamIcon style={{ fill: "#fff" }} />
            ) : (
              <VideocamOffIcon style={{ fill: "#fff" }} />
            )}
          </IconButton>
        </Box>
        <Box sx={{ mt: 2, display: "flex", gap: 2 }}>
          <Button
            size="large"
            variant="contained"
            color="primary"
            startIcon={<PlayCircleFilledIcon style={{ fill: "#fff" }} />}
            sx={{
              backgroundColor: "#12A150",
              "&:hover": {
                backgroundColor: "#007231",
              },
            }}
            onClick={onJoinSession}
          >
            Join Session
          </Button>
          <Button
            size="large"
            variant="contained"
            sx={{
              backgroundColor: "#CC525F",
              "&:hover": {
                backgroundColor: "#D53647",
              },
            }}
            startIcon={<CancelIcon style={{ fill: "#FFF" }} />}
            onClick={onCancel}
          >
            Cancel Session
          </Button>
        </Box>
      </Box>
    </Box>
  );
}

export default VideoCall;
