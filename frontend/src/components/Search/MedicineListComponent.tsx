// MedicineListComponent.tsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Pagination,
} from "@mui/material";
import api from "../../services/api";

interface Medicine {
  id: string;
  name: string;
  description: string;
  price: string;
  batch_number: string;
  unit_of_measurement: string;
  prescription_required: boolean;
  is_available: boolean;
  generic_name_details: { id: number; name: string };
  category_details: { id: number; name: string };
  form_details: { id: number; form_type: string };
  manufacturer_details: { id: number; name: string };
}

const MedicineListComponent: React.FC = () => {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);

  useEffect(() => {
    fetchMedicines();
  }, [page]);

  const fetchMedicines = async () => {
    try {
      const response = await api.get(`/medicines/`, { params: { page } });
      setMedicines(response.data.results);
      setTotalPages(Math.ceil(response.data.count / 10)); // Assuming page size of 10
    } catch (error) {
      console.error("Error fetching medicines:", error);
    }
  };

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  return (
    <Box padding={3}>
      <Typography variant="h4" gutterBottom>
        Medicines List
      </Typography>
      <TableContainer component={Paper} sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Batch Number</TableCell>
              <TableCell>Generic Name</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Form</TableCell>
              <TableCell>Manufacturer</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {medicines.map((medicine) => (
              <TableRow key={medicine.id}>
                <TableCell>{medicine.name}</TableCell>
                <TableCell>{medicine.description}</TableCell>
                <TableCell>{medicine.price}</TableCell>
                <TableCell>{medicine.batch_number}</TableCell>
                <TableCell>{medicine.generic_name_details?.name}</TableCell>
                <TableCell>{medicine.category_details?.name}</TableCell>
                <TableCell>{medicine.form_details?.form_type}</TableCell>
                <TableCell>{medicine.manufacturer_details?.name}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Box display="flex" justifyContent="center" marginTop={2}>
        <Pagination count={totalPages} page={page} onChange={handlePageChange} />
      </Box>
    </Box>
  );
};

export default MedicineListComponent;
