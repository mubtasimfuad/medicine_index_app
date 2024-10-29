import React, { useState, useEffect } from 'react';
import {
  Box, Button, TextField, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography, Snackbar, Alert
} from '@mui/material';
import api from '../../../../services/api';

interface GenericName {
  id: number;
  name: string;
}

const GenericNameTab: React.FC = () => {
  const [genericNames, setGenericNames] = useState<GenericName[]>([]);
  const [genericName, setGenericName] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

  useEffect(() => {
    const fetchGenericNames = async () => {
      try {
        const response = await api.get('/generic-names/');
        setGenericNames(response.data.data);
      } catch (error) {
        showErrorMessage('Error fetching generic names');
      }
    };
    fetchGenericNames();
  }, []);

  const handleAddGenericName = async () => {
    try {
      const response = await api.post('/generic-names/', { name: genericName });
      setGenericNames([...genericNames, response.data.data]);
      setGenericName('');
      showSuccessMessage('Generic name added successfully');
    } catch (error) {
      handleErrorMessage(error, 'Error adding generic name');
    }
  };

  const handleDeleteGenericName = async (id: number) => {
    try {
      await api.delete(`/generic-names/${id}/`);
      setGenericNames(genericNames.filter((name) => name.id !== id));
      showSuccessMessage('Generic name deleted successfully');
    } catch (error) {
      handleErrorMessage(error, 'Error deleting generic name');
    }
  };

  const showSuccessMessage = (message: string) => {
    setSnackbarMessage(message);
    setSnackbarSeverity('success');
    setSnackbarOpen(true);
  };

  const showErrorMessage = (message: string) => {
    setSnackbarMessage(message);
    setSnackbarSeverity('error');
    setSnackbarOpen(true);
  };

  const handleErrorMessage = (error: any, defaultMsg: string) => {
    if (error.response && error.response.status === 401) {
      showErrorMessage('Unauthorized access. Please log in.');
    } else {
      showErrorMessage(defaultMsg);
    }
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Manage Generic Names
      </Typography>
      <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" sx={{ mt: 2, mb: 3 }}>
        <TextField
          label="Generic Name"
          value={genericName}
          onChange={(e) => setGenericName(e.target.value)}
          margin="normal"
          fullWidth={false}
          sx={{ flexGrow: 1, minWidth: '200px' }}
        />
        <Button variant="contained" color="primary" onClick={handleAddGenericName} sx={{ minWidth: '120px' }}>
          Add Generic Name
        </Button>
      </Box>
      <TableContainer component={Paper} sx={{ overflowX: 'auto', mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Generic Name</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {genericNames.map((name) => (
              <TableRow key={name.id}>
                <TableCell>{name.name}</TableCell>
                <TableCell>
                  <Button color="secondary" onClick={() => handleDeleteGenericName(name.id)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Snackbar for success and error messages */}
      <Snackbar open={snackbarOpen} autoHideDuration={3000} onClose={handleSnackbarClose}>
        <Alert onClose={handleSnackbarClose} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default GenericNameTab;
