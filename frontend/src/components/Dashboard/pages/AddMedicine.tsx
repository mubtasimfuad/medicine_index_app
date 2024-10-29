import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Snackbar,
  Alert,
  CircularProgress,
} from "@mui/material";
import api from "../../../services/api";

const AddMedicine: React.FC = () => {
  const [medicineData, setMedicineData] = useState({
    name: "",
    generic_name: "",
    category: "",
    form: "",
    manufacturer: "",
    description: "",
    price: "",
    stock_quantity: "",
    batch_number: "",
    unit_of_measurement: "TBL",
    prescription_required: false,
    is_featured: false,
  });
  const [categories, setCategories] = useState<any[]>([]);
  const [forms, setForms] = useState<any[]>([]);
  const [manufacturers, setManufacturers] = useState<any[]>([]);
  const [genericNames, setGenericNames] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const fetchAuxiliaryData = async () => {
      setLoading(true);
      try {
        // Fetch categories, forms, manufacturers, and generic names in parallel
        const [categoriesRes, formsRes, manufacturersRes, genericNamesRes] = await Promise.all([
          api.get("/categories/"),
          api.get("/forms/"),
          api.get("/manufacturers/"),
          api.get("/generic-names/"),
        ]);

        // Set the state only once after all data is retrieved to avoid re-renders
        setCategories(categoriesRes.data.data || []);
        setForms(formsRes.data.data || []);
        setManufacturers(manufacturersRes.data.data || []);
        setGenericNames(genericNamesRes.data.data || []);
      } catch (error) {
        console.error("Error fetching auxiliary data:", error);
        setErrorMessage("Error fetching auxiliary data.");
      } finally {
        setLoading(false);
      }
    };

    // Call fetchAuxiliaryData once on component mount
    fetchAuxiliaryData();
  }, []); // Empty dependency array to run only once

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setMedicineData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setMedicineData((prevData) => ({
      ...prevData,
      [name]: checked,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post("/medicines/", medicineData);
      setSuccessMessage("Medicine added successfully!");
      setMedicineData({
        name: "",
        generic_name: "",
        category: "",
        form: "",
        manufacturer: "",
        description: "",
        price: "",
        stock_quantity: "",
        batch_number: "",
        unit_of_measurement: "TBL",
        prescription_required: false,
        is_featured: false,
      });
    } catch (error: any) {
      console.error("Error adding medicine:", error);
      const responseError = error.response?.data?.message;

      if (typeof responseError === "string") {
        setErrorMessage(responseError);
      } else if (responseError && typeof responseError === "object") {
        const errorMessages = Object.values(responseError).flat().join(" ");
        setErrorMessage(errorMessages || "Error adding medicine.");
      } else {
        setErrorMessage("Error adding medicine.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box padding={3}>
      <Typography variant="h4" gutterBottom>
        Add New Medicine
      </Typography>
      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
          <CircularProgress />
        </Box>
      ) : (
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            label="Name"
            name="name"
            value={medicineData.name}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          />
          <TextField
            select
            label="Generic Name"
            name="generic_name"
            value={medicineData.generic_name}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          >
            {genericNames.map((generic: any) => (
              <MenuItem key={generic.id} value={generic.id}>
                {generic.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Batch Number"
            name="batch_number"
            value={medicineData.batch_number}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          />
          <TextField
            label="Description"
            name="description"
            value={medicineData.description}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Price"
            name="price"
            type="number"
            value={medicineData.price}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          />
          <TextField
            label="Stock Quantity"
            name="stock_quantity"
            type="number"
            value={medicineData.stock_quantity}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          />
          <TextField
            select
            label="Category"
            name="category"
            value={medicineData.category}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          >
            {categories.map((category: any) => (
              <MenuItem key={category.id} value={category.id}>
                {category.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Form"
            name="form"
            value={medicineData.form}
            onChange={handleInputChange}
            fullWidth
            required
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
            value={medicineData.manufacturer}
            onChange={handleInputChange}
            fullWidth
            required
            margin="normal"
          >
            {manufacturers.map((manufacturer: any) => (
              <MenuItem key={manufacturer.id} value={manufacturer.id}>
                {manufacturer.name}
              </MenuItem>
            ))}
          </TextField>

          <FormControlLabel
            control={
              <Checkbox
                checked={medicineData.prescription_required}
                onChange={handleCheckboxChange}
                name="prescription_required"
              />
            }
            label="Prescription Required"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={medicineData.is_featured}
                onChange={handleCheckboxChange}
                name="is_featured"
              />
            }
            label="Featured Medicine"
          />

          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            disabled={submitting}
          >
            {submitting ? <CircularProgress size={24} /> : "Add Medicine"}
          </Button>
        </Box>
      )}

      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage("")}
      >
        <Alert onClose={() => setSuccessMessage("")} severity="success" sx={{ width: "100%" }}>
          {successMessage}
        </Alert>
      </Snackbar>

      <Snackbar
        open={!!errorMessage}
        autoHideDuration={6000}
        onClose={() => setErrorMessage("")}
      >
        <Alert onClose={() => setErrorMessage("")} severity="error" sx={{ width: "100%" }}>
          {errorMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default AddMedicine;
