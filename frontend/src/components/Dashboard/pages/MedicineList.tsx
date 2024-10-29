import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  IconButton,
  Snackbar,
  Alert,
  MenuItem,
} from "@mui/material";
import { Edit, Delete } from "@mui/icons-material";
import api from "../../../services/api";

const MedicineList: React.FC = () => {
  const [medicines, setMedicines] = useState([]);
  const [editData, setEditData] = useState<any>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [selectedIdToDelete, setSelectedIdToDelete] = useState<string | null>(
    null
  );
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [categories, setCategories] = useState([]);
  const [forms, setForms] = useState([]);
  const [manufacturers, setManufacturers] = useState([]);
  const [genericNames, setGenericNames] = useState([]);

  useEffect(() => {
    fetchMedicines();
    fetchAuxiliaryData();
  }, []);

  const fetchMedicines = async () => {
    try {
      const response = await api.get("/medicines/");
      setMedicines(response.data.data);
    } catch (error) {
      console.error("Error fetching medicines:", error);
    }
  };

  const fetchAuxiliaryData = async () => {
    try {
      const [categoriesRes, formsRes, manufacturersRes, genericNamesRes] =
        await Promise.all([
          api.get("/categories/"),
          api.get("/forms/"),
          api.get("/manufacturers/"),
          api.get("/generic-names/"),
        ]);
      setCategories(categoriesRes.data.data);
      setForms(formsRes.data.data);
      setManufacturers(manufacturersRes.data.data);
      setGenericNames(genericNamesRes.data.data);
    } catch (error) {
      console.error("Error fetching auxiliary data:", error);
    }
  };

  const handleDelete = async () => {
    if (selectedIdToDelete) {
      try {
        await api.delete(`/medicines/${selectedIdToDelete}/`);
        setMedicines(
          medicines.filter(
            (medicine: any) => medicine.id !== selectedIdToDelete
          )
        );
        setSuccessMessage("Medicine deleted successfully.");
      } catch (error) {
        console.error("Error deleting medicine:", error);
        setErrorMessage("Failed to delete medicine.");
      } finally {
        setShowDeleteConfirm(false);
        setSelectedIdToDelete(null);
      }
    }
  };

  const openEditModal = (medicine: any) => {
    setEditData({
      ...medicine,
      generic_name: medicine.generic_name_details?.id,
      category: medicine.category_details?.id,
      form: medicine.form_details?.id,
      manufacturer: medicine.manufacturer_details?.id,
    });
    setShowEditModal(true);
  };

  const handleEditSave = async () => {
    try {
      const payload = {
        id: editData.id,
        name: editData.name,
        description: editData.description,
        price: editData.price,
        batch_number: editData.batch_number,
        stock_quantity: editData.stock_quantity,
        unit_of_measurement: editData.unit_of_measurement,
        prescription_required: editData.prescription_required,
        is_available: editData.is_available,
        is_featured: editData.is_featured,
        generic_name: editData.generic_name,
        category: editData.category,
        form: editData.form,
        manufacturer: editData.manufacturer,
      };
      await api.put(`/medicines/${editData.id}/`, payload);
      setSuccessMessage("Medicine updated successfully.");
      fetchMedicines();
    } catch (error) {
      console.error("Error updating medicine:", error);
      setErrorMessage("Failed to update medicine.");
    } finally {
      setShowEditModal(false);
      setEditData(null);
    }
  };

  const handleEditChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setEditData((prevData: any) => ({ ...prevData, [name]: value }));
  };

  return (
    <Box padding={3}>
      <Typography variant="h4" gutterBottom>
        Medicines List
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Generic Name</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Form</TableCell>
              <TableCell>Manufacturer</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {medicines.map((medicine: any) => (
              <TableRow key={medicine.id}>
                <TableCell>{medicine.name}</TableCell>
                <TableCell>{medicine.generic_name_details?.name}</TableCell>
                <TableCell>{medicine.category_details?.name}</TableCell>
                <TableCell>{medicine.form_details?.form_type}</TableCell>
                <TableCell>{medicine.manufacturer_details?.name}</TableCell>
                <TableCell>{medicine.price}</TableCell>
                <TableCell>
                  <IconButton
                    color="primary"
                    onClick={() => openEditModal(medicine)}
                  >
                    <Edit />
                  </IconButton>
                  <IconButton
                    color="secondary"
                    onClick={() => {
                      setShowDeleteConfirm(true);
                      setSelectedIdToDelete(medicine.id);
                    }}
                  >
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Edit Medicine Modal */}
      {editData && (
        <Dialog
          open={showEditModal}
          onClose={() => setShowEditModal(false)}
          fullWidth
        >
          <DialogTitle>Edit Medicine</DialogTitle>
          <DialogContent>
            <TextField
              label="Name"
              name="name"
              value={editData.name}
              onChange={handleEditChange}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Price"
              name="price"
              value={editData.price}
              onChange={handleEditChange}
              fullWidth
              margin="normal"
              type="number"
            />
            <TextField
              select
              label="Generic Name"
              name="generic_name"
              value={editData.generic_name}
              onChange={handleEditChange}
              fullWidth
              margin="normal"
            >
              {genericNames.map((gen: any) => (
                <MenuItem key={gen.id} value={gen.id}>
                  {gen.name}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              select
              label="Category"
              name="category"
              value={editData.category}
              onChange={handleEditChange}
              fullWidth
              margin="normal"
            >
              {categories.map((cat: any) => (
                <MenuItem key={cat.id} value={cat.id}>
                  {cat.name}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              select
              label="Form"
              name="form"
              value={editData.form}
              onChange={handleEditChange}
              fullWidth
              margin="normal"
            >
              {forms.map((form: any) => (
                <MenuItem key={form.id} value={form.id}>
                  {form.form_type}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              select
              label="Manufacturer"
              name="manufacturer"
              value={editData.manufacturer}
              onChange={handleEditChange}
              fullWidth
              margin="normal"
            >
              {manufacturers.map((manu: any) => (
                <MenuItem key={manu.id} value={manu.id}>
                  {manu.name}
                </MenuItem>
              ))}
            </TextField>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowEditModal(false)} color="secondary">
              Cancel
            </Button>
            <Button onClick={handleEditSave} color="primary">
              Save
            </Button>
          </DialogActions>
        </Dialog>
      )}

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          Are you sure you want to delete this medicine?
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDeleteConfirm(false)} color="secondary">
            Cancel
          </Button>
          <Button onClick={handleDelete} color="primary">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Success and Error Messages */}
      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage("")}
      >
        <Alert
          onClose={() => setSuccessMessage("")}
          severity="success"
          sx={{ width: "100%" }}
        >
          {successMessage}
        </Alert>
      </Snackbar>

      <Snackbar
        open={!!errorMessage}
        autoHideDuration={6000}
        onClose={() => setErrorMessage(null)}
      >
        <Alert
          onClose={() => setErrorMessage(null)}
          severity="error"
          sx={{ width: "100%" }}
        >
          {errorMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MedicineList;
