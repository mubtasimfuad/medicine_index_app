import { styled } from "@mui/material/styles";
import { Box } from "@mui/material";

// Sidebar container with modern styling and contrast
export const SidebarContainer = styled(Box)(({ theme }) => ({
  width: "240px",
  height: "100vh",
  backgroundColor: theme.palette.grey[900],
  color: theme.palette.primary.contrastText,
  display: "flex",
  flexDirection: "column",
  padding: theme.spacing(2),
  boxShadow: "2px 0 5px rgba(0, 0, 0, 0.1)",
  [theme.breakpoints.down("md")]: {
    width: "100%",
    height: "auto",
    boxShadow: "none",
  },
}));

// Main content area with subtle background contrast and padding
export const ContentContainer = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  height: "100%",
  padding: theme.spacing(3),
  borderRadius: theme.shape.borderRadius,
  boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
  overflowY: "auto",
  [theme.breakpoints.down("md")]: {
    padding: theme.spacing(2),
  },
}));
