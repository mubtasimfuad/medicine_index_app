// src/styles/theme.ts

import { createTheme } from "@mui/material/styles";
import { grey, red } from "@mui/material/colors";

const theme = createTheme({
  palette: {
    mode: "light", // You can change this to 'dark' for a dark theme
    primary: {
      main: "#1E88E5", // Main brand color
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#FF4081",
      contrastText: "#FFFFFF",
    },
    error: {
      main: red[500],
    },
    background: {
      default: grey[50],
      paper: "#FFFFFF",
    },
    text: {
      primary: "#212121",
      secondary: grey[600],
    },
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
    h1: {
      fontSize: "2.2rem",
      fontWeight: 700,
      lineHeight: 1.3,
    },
    h2: {
      fontSize: "1.8rem",
      fontWeight: 700,
      lineHeight: 1.4,
    },
    h3: {
      fontSize: "1.6rem",
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.6,
      color: grey[800],
    },
    body2: {
      fontSize: "0.9rem",
      lineHeight: 1.6,
      color: grey[600],
    },
    button: {
      textTransform: "none", // Disable uppercase for buttons
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: "8px", // Rounded buttons
          fontWeight: "bold",
        },
        contained: {
          boxShadow: "none",
          "&:hover": {
            boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.2)",
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#FFFFFF",
          color: "#1E88E5",
          boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: "12px",
          boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            "& fieldset": {
              borderColor: grey[400],
            },
            "&:hover fieldset": {
              borderColor: "#1E88E5",
            },
            "&.Mui-focused fieldset": {
              borderColor: "#1E88E5",
            },
          },
        },
      },
    },
  },
});

export default theme;
