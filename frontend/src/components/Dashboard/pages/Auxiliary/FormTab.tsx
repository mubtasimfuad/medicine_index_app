import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Snackbar,
  Alert,
} from '@mui/material';
import api from '../../../../services/api';

interface FormType {
  id: number;
  form_type: string;
}

const FormTab: React.FC = () => {
  const [forms, setForms] = useState<FormType[]>([]);
  const [formType, setFormType] = useState('');
  const [editId, setEditId] = useState<number | null>(null);  // Track form being edited
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    fetchForms();
  }, []);

  const fetchForms = async () => {
    try {
      const response = await api.get('/forms/');
      setForms(response.data.data);
    } catch (error) {
      setErrorMessage('Error fetching forms');
    }
  };

  const handleAddOrUpdateForm = async () => {
    try {
      if (editId) {
        // Update form
        await api.put(`/forms/${editId}/`, { form_type: formType });
        setForms(forms.map((form) => (form.id === editId ? { ...form, form_type: formType } : form)));
        setEditId(null);
        setSuccessMessage('Form updated successfully');
      } else {
        // Create new form
        const response = await api.post('/forms/', { form_type: formType });
        setForms([...forms, response.data.data]);
        setSuccessMessage('Form added successfully');
      }
      setFormType('');
    } catch (error) {
      setErrorMessage('Error adding/updating form');
    }
  };

  const handleEditForm = (form: FormType) => {
    setEditId(form.id);
    setFormType(form.form_type);
  };

  const handleDeleteForm = async (id: number) => {
    try {
      await api.delete(`/forms/${id}/`);
      setForms(forms.filter((form) => form.id !== id));
      setSuccessMessage('Form deleted successfully');
    } catch (error) {
      setErrorMessage('Error deleting form');
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Manage Forms
      </Typography>
      <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" sx={{ mt: 2, mb: 3 }}>
        <TextField
          label="Form Type"
          value={formType}
          onChange={(e) => setFormType(e.target.value)}
          margin="normal"
          fullWidth={false}
          sx={{ flexGrow: 1, minWidth: '200px' }}
        />
        <Button variant="contained" color="primary" onClick={handleAddOrUpdateForm} sx={{ minWidth: '120px' }}>
          {editId ? 'Update Form' : 'Add Form'}
        </Button>
      </Box>
      <TableContainer component={Paper} sx={{ overflowX: 'auto', mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Form Type</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {forms.map((form) => (
              <TableRow key={form.id}>
                <TableCell>{form.form_type}</TableCell>
                <TableCell>
                  <Button color="primary" onClick={() => handleEditForm(form)}>
                    Edit
                  </Button>
                  <Button color="secondary" onClick={() => handleDeleteForm(form.id)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Success Snackbar */}
      <Snackbar open={!!successMessage} autoHideDuration={6000} onClose={() => setSuccessMessage('')}>
        <Alert onClose={() => setSuccessMessage('')} severity="success" sx={{ width: '100%' }}>
          {successMessage}
        </Alert>
      </Snackbar>

      {/* Error Snackbar */}
      <Snackbar open={!!errorMessage} autoHideDuration={6000} onClose={() => setErrorMessage('')}>
        <Alert onClose={() => setErrorMessage('')} severity="error" sx={{ width: '100%' }}>
          {errorMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default FormTab;
