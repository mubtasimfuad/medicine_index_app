import React, { useState } from 'react';
import { Box, Typography, Container, Snackbar, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LoginContainer, FormContainer, StyledTextField, StyledButton, Title, ForgotPasswordLink } from './Login.styles';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);  // State for showing error
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Call login API
      const response = await axios.post('http://localhost:8000/api/auth/login/', {
        username,
        password,
      });

      // Store access and refresh tokens in local storage
      const { access, refresh } = response.data;
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);

      // Redirect to dashboard after successful login
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials, please try again.');
      setOpenSnackbar(true);  // Show error message
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
            <StyledButton type="submit" fullWidth variant="contained">
              Sign In
            </StyledButton>
          </Box>
          <Typography align="center" variant="body2">
            <ForgotPasswordLink href="#">Forgot Password?</ForgotPasswordLink>
          </Typography>
        </FormContainer>
      </Container>

      {/* Error Snackbar */}
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </LoginContainer>
  );
};

export default Login;
