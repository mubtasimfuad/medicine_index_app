// Login.tsx
import React, { useState } from "react";
import { Box, Typography, Container, Snackbar, Alert, CircularProgress } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../services/AuthContext";
import { LoginContainer, FormContainer, StyledTextField, StyledButton, Title, ForgotPasswordLink } from "./Login.styles";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // Add loading state
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const { login } = useAuth(); // Get login function from AuthContext
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); // Set loading to true when login starts
    try {
      const response = await axios.post("/api/auth/login/", {
        username,
        password,
      });

      const { access, refresh } = response.data;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);

      login(); // Update auth state
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid credentials, please try again.");
      setOpenSnackbar(true);
    } finally {
      setLoading(false); // Reset loading state after request completion
    }
  };

  return (
    <LoginContainer>
      <Container maxWidth="xs">
        <FormContainer>
          <Title variant="h3" gutterBottom align="center">
            Login
          </Title>
          <Typography variant="subtitle1" align="center" gutterBottom color="white">
            Please sign in to access your dashboard
          </Typography>
          <Box component="form" onSubmit={handleLogin}>
            <StyledTextField
              label="Username"
              variant="outlined"
              fullWidth
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <StyledTextField
              label="Password"
              type="password"
              variant="outlined"
              fullWidth
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <StyledButton type="submit" fullWidth variant="contained" disabled={loading}>
              {loading ? <CircularProgress size={24} color="inherit" /> : "Sign In"}
            </StyledButton>
          </Box>
          <Typography align="center" variant="body2">
            <ForgotPasswordLink href="#">Forgot Password?</ForgotPasswordLink>
          </Typography>
        </FormContainer>
      </Container>

      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity="error" sx={{ width: "100%" }}>
          {error}
        </Alert>
      </Snackbar>
    </LoginContainer>
  );
};

export default Login;
