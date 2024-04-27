import React, { useState } from "react";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import TextareaAutosize from "@mui/material/TextareaAutosize";
import Button from "@mui/material/Button";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import { useTheme, FormGroup } from "@mui/material";
import { useRouter } from "next/router";
import CancelIcon from "@mui/icons-material/Cancel";
import PlayCircleFilledIcon from "@mui/icons-material/PlayCircleFilled";
import { SessionType } from "@/Enums/SessionType";
import { NaturePeopleSharp } from "@mui/icons-material";

interface PracticeSessionModalProps {
  open: boolean;
  onClose: () => void;
  sessionType: SessionType;
}

function renderSelect(
  label: string,
  value: string,
  setValue: React.Dispatch<React.SetStateAction<string>>,
  options: { value: string; label: string }[]
) {
  return (
    <FormControl fullWidth margin="normal">
      <InputLabel>{label}</InputLabel>
      <Select value={value} label={label} onChange={(e) => setValue(e.target.value as string)}>
        {options.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}

const StartPracticeSessionModel: React.FC<PracticeSessionModalProps> = ({
  open,
  onClose,
  sessionType,
}) => {
  // State for form fields
  const [practiceSetId, setPracticeSetId] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [interviewType, setInterviewType] = useState("");
  const [interviewDuration, setInterviewDuration] = useState("");
  const [questionMode, setQuestionMode] = useState("");
  const [interviewTone, setInterviewTone] = useState("");
  const [resume, setResume] = useState("");
  const router = useRouter();

  const theme = useTheme();

  const interviewTypeOptions = [
    { value: "behavioral", label: "Behavioral/HR Interview" },
    { value: "technical", label: "Technical Interview" },
    { value: "conversational", label: "Conversational Interview" },
    { value: "stress", label: "Stress Interview" },
  ];

  const interviewDurationOptions = [
    { value: "short", label: "Short (2-3 Questions)" },
    { value: "medium", label: "Medium (5-6 Questions)" },
    { value: "long", label: "Long (8-10 Questions)" },
  ];

  const questionModeOptions = [
    { value: "unseen", label: "Unseen" },
    { value: "predefined", label: "Predefined" },
    { value: "mixed", label: "Mixed" },
  ];

  const interviewToneOptions = [
    { value: "friendly", label: "Friendly" },
    { value: "neutral", label: "Neutral" },
    { value: "strict", label: "Strict" },
  ];

  const desiredToneOptions = [
    { value: "friendly", label: "Friendly" },
    { value: "neutral", label: "Neutral" },
    { value: "strict", label: "Strict" },
    { value: "persuasive", label: "Persuasive" },
    { value: "natural", label: "Natural" },
    { value: "authoritative", label: "Authoritative" },
    { value: "inspirational", label: "Inspirational" },
    { value: "educational", label: "Educational" },
    { value: "formal", label: "Formal" },
    { value: "informal", label: "Informal" },
    { value: "enthusiastic", label: "Enthusiastic" },
    { value: "empathetic", label: "Empathetic" },
    { value: "humorous", label: "Humorous" },
  ];

  const resumeOptions = [
    { value: "Faaiz_Resume.pdf", label: "Faaiz_Resume.pdf" },
    { value: "Maher_CV.pdf", label: "Maher_CV.pdf" },
  ];

  const onSubmit = () => {
    onClose();
    // Use encodeURIComponent to ensure spaces are encoded as %20
    const encodedSessionType = encodeURIComponent(sessionType);
    router.push({
      pathname: "/live-practice-session",
      query: { sessionType: encodedSessionType },
    });
  };
  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "40rem",
          bgcolor: "background.paper",
          p: 4,
          borderRadius: 2,
        }}
      >
        <Typography variant="h6" component="h2" textAlign="center">
          Start New {sessionType}
        </Typography>
        <FormGroup>
          <TextField
            label="Practice Set ID:"
            variant="outlined"
            margin="normal"
            fullWidth
            value={practiceSetId}
            onChange={(e) => setPracticeSetId(e.target.value)}
          />
          {sessionType === SessionType.MockInterview ? (
            <>
              <TextField
                label="Job Title"
                variant="outlined"
                margin="normal"
                fullWidth
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
              />
              <TextField
                fullWidth
                label="Job Description"
                variant="outlined"
                margin="normal"
                multiline
                rows={3}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
              {renderSelect(
                "Interview Type",
                interviewType,
                setInterviewType,
                interviewTypeOptions
              )}
              {renderSelect(
                "Interview Duration",
                interviewDuration,
                setInterviewDuration,
                interviewDurationOptions
              )}
              {renderSelect("Question Mode", questionMode, setQuestionMode, questionModeOptions)}
              {renderSelect(
                "Interview Tone",
                interviewTone,
                setInterviewTone,
                interviewToneOptions
              )}
              {renderSelect("Resume", resume, setResume, resumeOptions)}
            </>
          ) : (
            <>
              <TextField
                label="Practice Title"
                variant="outlined"
                margin="normal"
                fullWidth
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
              />
              <TextField
                fullWidth
                label="Goal Description"
                variant="outlined"
                margin="normal"
                multiline
                rows={3}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />

              {renderSelect("Desired Tone", interviewTone, setInterviewTone, desiredToneOptions)}
            </>
          )}
        </FormGroup>
        <Box sx={{ display: "flex", justifyContent: "center", width: "100%", mt: 2, gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<CancelIcon style={{ fill: theme.palette.primary.main }} />}
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            startIcon={<PlayCircleFilledIcon style={{ fill: "#fff" }} />}
            onClick={onSubmit}
          >
            Start
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default StartPracticeSessionModel;
