import React, { useState } from "react";
import { Box, Button, Grid, TextField, Typography, IconButton, Avatar } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import SaveIcon from "@mui/icons-material/Save";
import CameraAltIcon from "@mui/icons-material/CameraAlt";
import { Image } from "@mui/icons-material";

export default function AccountsPage() {
  const [isEditable, setIsEditable] = useState(false);
  const [profile, setProfile] = useState({
    firstName: "Faaiz",
    lastName: "khan",
    email: "faaiz.khan@example.com",
    phoneNumber: "+905527174697",
    password: "password123",
    aboutMe:
      "I'm Faaiz an innovative and dynamic junior Computer Engineering major at Bilkent University (Turkey). As an entrepreneurially-minded and solution-focused individual, I bring a wealth of experience in Automation/Scripting, Full-Stack, Android app, Desktop application, and Software Development to the table. My passion for intricate and challenging programming problems drives me to excel and deliver exceptional results. ",
    skills: "React, Material-UI, JavaScript",
  });

  // Handlers
  const handleEditSave = () => {
    setIsEditable(!isEditable);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setProfile({ ...profile, [name]: value });
  };

  return (
    <Box sx={{ flexGrow: 1, p: 4 }}>
      <Typography variant="h2" align="center" gutterBottom>
        Account
      </Typography>
      <Grid container spacing={2}>
        {/* Left side fields */}
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="First Name"
            variant="outlined"
            value={profile.firstName}
            onChange={handleChange}
            name="firstName"
            disabled={!isEditable}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Last Name"
            variant="outlined"
            value={profile.lastName}
            onChange={handleChange}
            name="lastName"
            disabled={!isEditable}
            margin="normal"
          />
          <TextField
            disabled
            fullWidth
            label="Email"
            variant="outlined"
            value={profile.email}
            onChange={handleChange}
            name="email"
            margin="normal"
          />
          <TextField
            fullWidth
            label="Phone Number"
            variant="outlined"
            value={profile.phoneNumber}
            onChange={handleChange}
            name="phoneNumber"
            disabled
            margin="normal"
          />
          <TextField
            fullWidth
            label="Password"
            variant="outlined"
            value={profile.password}
            onChange={handleChange}
            name="password"
            disabled={!isEditable}
            margin="normal"
            type="password"
          />
        </Grid>

        {/* Right side profile picture */}
        <Grid
          item
          xs={12}
          md={6}
          sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}
        >
          <Avatar src="/user-avatar.svg" sx={{ width: 300, height: 300, mb: 2 }} />
          <Box sx={{ display: "flex", gap: 1 }}>
            <Button
              size="large"
              variant="contained"
              sx={{ textTransform: "none", height: "fit-content" }}
              startIcon={<Image style={{ fill: "#fff" }} />}
            >
              Change Photo
            </Button>
            <IconButton
              sx={{
                backgroundColor: "error.main",
                "&:hover": {
                  backgroundColor: "error.dark",
                },
              }}
            >
              <DeleteIcon sx={{ fill: "#fff" }} />
            </IconButton>
          </Box>
        </Grid>

        {/* Full width fields */}
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="About Me"
            variant="outlined"
            value={profile.aboutMe}
            onChange={handleChange}
            name="aboutMe"
            disabled={!isEditable}
            multiline
            rows={4}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Skills"
            variant="outlined"
            value={profile.skills}
            onChange={handleChange}
            name="skills"
            disabled={!isEditable}
            multiline
            margin="normal"
          />
        </Grid>

        {/* Edit/Save Button */}
        <Grid item xs={12} sx={{ display: "flex", justifyContent: "center" }}>
          <Button
            startIcon={
              isEditable ? <SaveIcon sx={{ fill: "#fff" }} /> : <EditIcon sx={{ fill: "#fff" }} />
            }
            onClick={handleEditSave}
            variant="contained"
            size="large"
            sx={{ mt: 2, width: 300 }}
          >
            {isEditable ? "Save" : "Edit"}
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
}
