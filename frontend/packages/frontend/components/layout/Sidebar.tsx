import * as React from "react";
import { styled, useTheme, Theme, CSSObject } from "@mui/material/styles";
import Box from "@mui/material/Box";
import MuiDrawer from "@mui/material/Drawer";
import MuiAppBar, { AppBarProps as MuiAppBarProps } from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/MenuOutlined";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeftOutlined";
import ChevronRightIcon from "@mui/icons-material/ChevronRightOutlined";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUpOutlined";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDownOutlined";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInboxOutlined";
import MailIcon from "@mui/icons-material/MailOutline";
import DashboardIcon from "@mui/icons-material/DashboardOutlined";
import AccountCircleIcon from "@mui/icons-material/AccountCircleOutlined";
import DescriptionIcon from "@mui/icons-material/DescriptionOutlined";
// For QuizIcon and MenuBookIcon, outlined versions are not directly named in the material icons, so using placeholders or nearest match
import QuizIcon from "@mui/icons-material/QuizOutlined"; // Assuming there's an outlined version
import HistoryIcon from "@mui/icons-material/HistoryOutlined";
import AnalyticsIcon from "@mui/icons-material/AnalyticsOutlined";
import Tooltip from "@mui/material/Tooltip";
import MenuBookIcon from "@mui/icons-material/MenuBookOutlined"; // Assuming there's an outlined version
import { Menu } from "@mui/base/Menu";
import { red, green } from "@mui/material/colors";
import { Collapse, ListSubheader } from "@mui/material";
import { StarBorder } from "@mui/icons-material";
import { useRouter } from "next/router";
import SettingsIcon from "@mui/icons-material/SettingsOutlined";
import LogoutIcon from "@mui/icons-material/LogoutOutlined";
// For logouticon, assuming an import error since it's not from @mui/icons-material
// Adjust TuneIcon, NotificationsIcon, IntegrationInstructionsIcon, VideocamIcon, and SecurityIcon to outlined versions
import TuneIcon from "@mui/icons-material/TuneOutlined"; // Assuming there's an outlined version
import NotificationsIcon from "@mui/icons-material/NotificationsOutlined";
import IntegrationInstructionsIcon from "@mui/icons-material/IntegrationInstructionsOutlined"; // Assuming there's an outlined version
import VideocamIcon from "@mui/icons-material/VideocamOutlined";
import SecurityIcon from "@mui/icons-material/SecurityOutlined";

const drawerWidth = 240;

const openedMixin = (theme: Theme): CSSObject => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== "open" })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: "nowrap",
    boxSizing: "border-box",
    ...(open
      ? {
          ...openedMixin(theme),
          "& .MuiDrawer-paper": {
            ...openedMixin(theme),
            overflowX: "visible", // Allow horizontal overflow when drawer is open
            overflowY: "hidden", // Keep vertical overflow hidden to avoid scroll bars on the y-axis
            zIndex: 1200, // Ensures it is above most content but adjust based on your app's z-index management
          },
        }
      : {
          ...closedMixin(theme),
          "& .MuiDrawer-paper": {
            ...closedMixin(theme),
            overflowX: "visible", // Allow horizontal overflow when drawer is closed
            overflowY: "hidden", // Maintain vertical overflow settings
            zIndex: 1200, // Adjust zIndex if necessary to ensure visibility
          },
        }),
  })
);

export default function SideBar({ updateSideBarWidth }) {
  const theme = useTheme();
  const [open, setOpen] = React.useState(true);
  const router = useRouter(); // Using useRouter hook here
  const [openSettings, setOpenSettings] = React.useState(false);

  React.useEffect(() => {
    updateSideBarWidth(true);
  }, []);

  const settingsItems = [
    {
      title: "App Preferences",
      icon: <TuneIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "app-preferences",
    },
    {
      title: "Integrations",
      icon: <IntegrationInstructionsIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "integrations",
    },
    {
      title: "Audio/Video",
      icon: <VideocamIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "audio-video-settings",
    },
    {
      title: "Security",
      icon: <SecurityIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "security",
    },
  ];

  const menuItems = [
    {
      title: "Dashboard",
      icon: <DashboardIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "dashboard",
    },
    {
      title: "Account",
      icon: <AccountCircleIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "account",
    },
    {
      title: "Resumes",
      icon: <DescriptionIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "resumes",
    },
    {
      title: "Preparation Set",
      icon: <QuizIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "preparation-sets",
    },
    {
      title: "Past Sessions",
      icon: <HistoryIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "past-sessions",
    },
    {
      title: "Analytics",
      icon: <AnalyticsIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "analytics",
    },
    {
      title: "Practice Guide",
      icon: <MenuBookIcon style={{ fill: theme.palette.text.secondary }} />,
      page: "practice-guide",
    },
  ];

  const toggleDrawer = () => {
    setOpen(!open);
    updateSideBarWidth(!open);
  };

  const handleToggleSettings = () => {
    setOpenSettings(!openSettings);
  };

  const handleMenuItemClick = (page: string) => {
    router.push(`/${page}`); // Assuming your `page` values in menuItems are valid paths
  };

  const logout = () => {
    router.push(`/login`); // Assuming your `page` values in menuItems are valid paths
  };

  return (
    <Box sx={{ display: "flex" }}>
      {/* <CssBaseline /> */}
      <Drawer
        variant="permanent"
        open={open}
        sx={{
          "& .MuiDrawer-paper": {
            backgroundColor: theme.palette.background.default,
            marginLeft: 1,
            marginTop: 7,
            marginRight: 5,
            borderRadius: 5,
            maxHeight: "calc(100vh - 80px)",
            minHeight: "calc(100vh - 64px)",
            overflowY: "auto", // Enables vertical scrolling
            overflowX: "hidden",
          },
        }}
      >
        {!open && (
          <DrawerHeader>
            <IconButton
              onClick={toggleDrawer}
              sx={{
                backgroundColor: theme.palette.primary.main,
              }}
            >
              <ChevronRightIcon style={{ fill: "#FFF" }} />
            </IconButton>
          </DrawerHeader>
        )}
        <List>
          {menuItems.map((item, index) => (
            <Tooltip key={item.title} title={!open ? item.title : ""} placement="right">
              <ListItem key={item.title} disablePadding sx={{ display: "block" }}>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    width: "100%",
                    alignItems: "center",
                    position: "relative", // Needed for absolute positioning of the toggle button
                  }}
                >
                  <ListItemButton
                    onClick={() => handleMenuItemClick(item.page)} // Added onClick event here
                    sx={{
                      minHeight: 48,
                      justifyContent: open ? "initial" : "center",
                      px: 2.5,
                      "&:hover": {
                        backgroundColor: theme.palette.action.hover,
                      },
                    }}
                  >
                    <ListItemIcon
                      sx={{
                        minWidth: 0,
                        mr: open ? 3 : "auto",
                        justifyContent: "center",
                      }}
                    >
                      {item.icon}
                    </ListItemIcon>
                    {open && (
                      <ListItemText
                        primary={item.title}
                        primaryTypographyProps={{ style: { color: theme.palette.text.secondary } }}
                      />
                    )}
                  </ListItemButton>
                  {index == 0 && open && (
                    <IconButton
                      onClick={toggleDrawer}
                      sx={{
                        position: "absolute",
                        right: "-10px",
                        top: "30px",
                        border: 1,
                        borderRadius: 3,
                        zIndex: 1,
                        backgroundColor: theme.palette.primary.main,
                        color: "#FFF",
                        "&:hover": {
                          backgroundColor: theme.palette.info.main,
                        },
                      }}
                    >
                      {!open ? (
                        <ChevronRightIcon style={{ fill: "#FFF" }} />
                      ) : (
                        <ChevronLeftIcon style={{ fill: "#FFF" }} />
                      )}
                    </IconButton>
                  )}
                </Box>
              </ListItem>
            </Tooltip>
          ))}
          <Divider />
          <Tooltip key={"Settings"} title={!open ? "Settings" : ""} placement="right">
            <ListItemButton onClick={handleToggleSettings}>
              <ListItemIcon>
                <SettingsIcon style={{ marginLeft: "3px", fill: theme.palette.text.secondary }} />
              </ListItemIcon>
              <ListItemText
                primary="Settings"
                primaryTypographyProps={{ style: { color: theme.palette.text.secondary } }}
              />
              <IconButton onClick={handleToggleSettings}>
                {openSettings ? (
                  <KeyboardArrowUpIcon style={{ fill: theme.palette.text.secondary }} />
                ) : (
                  <KeyboardArrowDownIcon style={{ fill: theme.palette.text.secondary }} />
                )}
              </IconButton>
            </ListItemButton>
          </Tooltip>
          <Collapse in={openSettings} timeout="auto" unmountOnExit>
            <Divider />
            <List component="div" disablePadding>
              {settingsItems.map((item) => (
                <Tooltip key={item.title} title={!open ? item.title : ""} placement="right">
                  <ListItemButton
                    key={item.title}
                    sx={{ pl: 2.5 }}
                    onClick={() => handleMenuItemClick(item.page)}
                  >
                    <ListItemIcon>{item.icon}</ListItemIcon>
                    <ListItemText
                      primary={item.title}
                      primaryTypographyProps={{ style: { color: theme.palette.text.secondary } }}
                    />
                  </ListItemButton>
                </Tooltip>
              ))}
            </List>
          </Collapse>
        </List>
        <Divider />
        {/* Logout Button */}
        <List
          sx={{
            mt: "auto",
            // paddingLeft: 1,
          }}
        >
          <Tooltip key={"Logout"} title={!open ? "Logout" : ""} placement="right">
            <ListItemButton
              onClick={logout}
              sx={{
                "&:hover": {
                  backgroundColor: theme.palette.error.light,
                },
              }}
            >
              <ListItemIcon>
                <LogoutIcon style={{ fill: theme.palette.error.main }} />
              </ListItemIcon>
              <ListItemText
                primary="Logout"
                primaryTypographyProps={{ style: { color: theme.palette.error.main } }}
              />
            </ListItemButton>
          </Tooltip>
        </List>
      </Drawer>
    </Box>
  );
}
