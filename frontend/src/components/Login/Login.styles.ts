import { styled } from '@mui/material/styles';
import { Box, TextField, Button, Typography, Link } from '@mui/material';

// URL of the background image
const backgroundImageUrl = 'https://patient.info/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fxxv4b9mbhlgd%2F1MJNHM6uoxakC7rNL4mIAV%2F6bb317b1d835233a377a3b9c601f9b5e%2Fmedicines-a-z.png&w=1600&q=75';

export const LoginContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  height: '100vh',
  backgroundImage: `url(${backgroundImageUrl})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
  position: 'relative',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent overlay
    backdropFilter: 'blur(10px)', // Blur effect
    zIndex: 1,
  },
}));

export const FormContainer = styled(Box)(({ theme }) => ({
  position: 'relative',
  zIndex: 2, // Ensures the form stays above the blurred background
  backgroundColor: theme.palette.grey[900],
  padding: theme.spacing(6),
  borderRadius: theme.shape.borderRadius,
  boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.2)',
  width: '100%',
  maxWidth: '400px',
  textAlign: 'center',
}));

export const Title = styled(Typography)(({ theme }) => ({
  color: theme.palette.primary.contrastText,
  fontSize: '1.5rem',
  fontWeight: 500,
  marginBottom: theme.spacing(3),
}));

export const StyledTextField = styled(TextField)(({ theme }) => ({
  '& .MuiInputBase-root': {
    backgroundColor: theme.palette.grey[800],
    color: theme.palette.primary.contrastText,
    '&:-webkit-autofill': {
      WebkitBoxShadow: `0 0 0px 1000px ${theme.palette.grey[800]} inset`,
      WebkitTextFillColor: theme.palette.primary.contrastText,
    },
  },
  '& .MuiInputLabel-root': {
    color: theme.palette.grey[500],
  },
  '& .MuiInputLabel-root.Mui-focused': {
    color: theme.palette.primary.main,
  },
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: theme.palette.grey[700],
    },
    '&:hover fieldset': {
      borderColor: theme.palette.primary.main,
    },
    '&.Mui-focused fieldset': {
      borderColor: theme.palette.primary.main,
    },
  },
  marginBottom: theme.spacing(2),
}));

export const StyledButton = styled(Button)(({ theme }) => ({
  backgroundColor: theme.palette.error.main,
  color: theme.palette.common.white,
  fontWeight: 'bold',
  marginTop: theme.spacing(2),
  padding: theme.spacing(1.5),
  '&:hover': {
    backgroundColor: theme.palette.error.dark,
  },
}));

export const ForgotPasswordLink = styled(Link)(({ theme }) => ({
  display: 'block',
  marginTop: theme.spacing(1),
  color: theme.palette.grey[300],
  textDecoration: 'underline',
  '&:hover': {
    color: theme.palette.primary.light,
  },
}));
