import React, { useEffect, useState } from 'react';
import { Box, Button, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../../../services/api';

const MedicineList: React.FC = () => {
  const [medicines, setMedicines] = useState([]);

  useEffect(() => {
    const fetchMedicines = async () => {
      try {
        const response = await api.get('/medicines/');
        setMedicines(response.data.data); // Assuming 'data' key holds medicine data from API response
      } catch (error) {
        console.error('Error fetching medicines:', error);
      }
    };
    fetchMedicines();
  }, []);

  const handleDelete = async (id: string) => {
    try {
      await api.delete(`/medicines/${id}/`);
      setMedicines(medicines.filter((medicine: any) => medicine.id !== id)); // Update state to reflect deletion
    } catch (error) {
      console.error('Error deleting medicine:', error);
    }
  };
  

  return (
    <Box padding={3}>
      <Typography variant="h4" gutterBottom>
        Medicines List
      </Typography>
      <Button variant="contained" color="primary" component={Link} to="/dashboard/add-medicine">
        Add New Medicine
      </Button>
      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Generic Name</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {medicines.map((medicine: any) => (
              <TableRow key={medicine.id}>
                <TableCell>{medicine.name}</TableCell>
                <TableCell>{medicine.generic_name.name}</TableCell>
                <TableCell>{medicine.category.name}</TableCell>
                <TableCell>{medicine.price}</TableCell>
                <TableCell>
                  <Button color="primary" component={Link} to={`/dashboard/medicine/edit/${medicine.id}`}>
                    Edit
                  </Button>
                  <Button color="secondary" onClick={() => handleDelete(medicine.id)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default MedicineList;
