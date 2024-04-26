import React, { useState, useRef, useEffect } from "react";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import PlayCircle from "@mui/icons-material/PlayCircle";
import { useTheme } from "@mui/material/styles";
import { SessionType } from "@/Enums/SessionType";

interface PracticeSessionButtonProps {
  onSelect: (sessionType: SessionType) => void;
}

const PracticeSessionButton: React.FC<PracticeSessionButtonProps> = ({ onSelect }) => {
  const theme = useTheme();
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [menuWidth, setMenuWidth] = useState<number | undefined>(undefined);
  const [showDropDownMenu, setShowDropDownMenu] = useState<null | HTMLElement>(null);
  const open = Boolean(showDropDownMenu);

  const handleSelect = (sessionType: SessionType) => {
    // Parameter type as enum
    onSelect(sessionType);
    handleClose();
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setShowDropDownMenu(event.currentTarget);
    updateMenuWidth();
  };

  const handleClose = () => {
    setShowDropDownMenu(null);
  };

  const updateMenuWidth = () => {
    if (buttonRef.current) {
      setMenuWidth(buttonRef.current.clientWidth);
    }
  };

  useEffect(() => {
    const handleResize = () => {
      updateMenuWidth();
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <>
      <Button
        ref={buttonRef}
        size="small"
        variant="contained"
        sx={{ textTransform: "none", height: "fit-content" }}
        startIcon={<PlayCircle style={{ fill: "#fff" }} />}
        onClick={handleClick}
      >
        Start New Practice Session
      </Button>
      <Menu
        id="practice-menu"
        anchorEl={showDropDownMenu}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          "aria-labelledby": "basic-button",
        }}
        sx={{
          "& .MuiPaper-root": {
            width: menuWidth,
          },
        }}
      >
        <MenuItem onClick={() => handleSelect(SessionType.QuickStart)}>
          {SessionType.QuickStart}
        </MenuItem>
        <MenuItem onClick={() => handleSelect(SessionType.MockInterview)}>
          {SessionType.MockInterview}
        </MenuItem>
        <MenuItem onClick={() => handleSelect(SessionType.PresentationPractice)}>
          {SessionType.PresentationPractice}
        </MenuItem>
        <MenuItem onClick={() => handleSelect(SessionType.SalesPitch)}>
          {SessionType.SalesPitch}
        </MenuItem>
        <MenuItem
          onClick={() => handleSelect(SessionType.UploadVideo)}
          sx={{
            backgroundColor: theme.palette.action.hover,
            "&:hover": {
              backgroundColor: theme.palette.text.secondary,
              color: theme.palette.action.hover,
            },
          }}
        >
          {SessionType.UploadVideo}
        </MenuItem>
      </Menu>
    </>
  );
};

export default PracticeSessionButton;
