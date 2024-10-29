import React, { useState, useEffect } from "react";
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
  CircularProgress,
  IconButton,
} from "@mui/material";
import { Edit, Delete } from "@mui/icons-material";
import api from "../../../../services/api";

interface Manufacturer {
  id: number;
  name: string;
  contact_info?: string;
  website?: string;
  logo?: string;
}

const ManufacturerTab: React.FC = () => {
  const [manufacturers, setManufacturers] = useState<Manufacturer[]>([]);
  const [name, setName] = useState("");
  const [contactInfo, setContactInfo] = useState("");
  const [website, setWebsite] = useState("");
  const [logo, setLogo] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);

  const MEDIA_URL = "http://localhost:8000";

  useEffect(() => {
    fetchManufacturers();
  }, []);

  const fetchManufacturers = async () => {
    setLoading(true);
    try {
      const response = await api.get("/manufacturers/");
      setManufacturers(response.data.data); // Adjusted to use full data set from backend
    } catch (error) {
      console.error("Error fetching manufacturers:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddOrUpdateManufacturer = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("contact_info", contactInfo);
      formData.append("website", website);
      if (logo) formData.append("logo", logo);

      if (editId) {
        await api.put(`/manufacturers/${editId}/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setEditId(null);
      } else {
        const response = await api.post("/manufacturers/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setManufacturers((prev) => [...prev, response.data.data]);
      }

      // Reset form inputs
      setName("");
      setContactInfo("");
      setWebsite("");
      setLogo(null);
      fetchManufacturers(); // Refresh the list
    } catch (error) {
      console.error("Error adding/updating manufacturer:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditManufacturer = (manufacturer: Manufacturer) => {
    setEditId(manufacturer.id);
    setName(manufacturer.name);
    setContactInfo(manufacturer.contact_info || "");
    setWebsite(manufacturer.website || "");
  };

  const handleDeleteManufacturer = async (id: number) => {
    try {
      await api.delete(`/manufacturers/${id}/`);
      setManufacturers(
        manufacturers.filter((manufacturer) => manufacturer.id !== id)
      );
    } catch (error) {
      console.error("Error deleting manufacturer:", error);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Manage Manufacturers
      </Typography>
      <Box
        display="flex"
        flexDirection="column"
        gap={2}
        mb={3}
        sx={{ maxWidth: "600px" }}
      >
        <TextField
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <TextField
          label="Contact Info"
          value={contactInfo}
          onChange={(e) => setContactInfo(e.target.value)}
        />
        <TextField
          label="Website"
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
          type="url"
        />
        <Button variant="contained" component="label">
          Upload Logo
          <input
            type="file"
            hidden
            onChange={(e) => setLogo(e.target.files ? e.target.files[0] : null)}
          />
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleAddOrUpdateManufacturer}
        >
          {editId ? "Update Manufacturer" : "Add Manufacturer"}
        </Button>
      </Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Contact Info</TableCell>
                <TableCell>Website</TableCell>
                <TableCell>Logo</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {manufacturers.map((manufacturer) => (
                <TableRow key={manufacturer.id}>
                  <TableCell>{manufacturer.name}</TableCell>
                  <TableCell>{manufacturer.contact_info}</TableCell>
                  <TableCell>{manufacturer.website}</TableCell>
                  <TableCell>
                    {manufacturer.logo ? (
                      <img
                        src={
                          manufacturer.logo.startsWith("http")
                            ? manufacturer.logo
                            : `${MEDIA_URL}${manufacturer.logo}`
                        }
                        alt={`${manufacturer.name} logo`}
                        style={{ width: "50px", height: "50px" }}
                      />
                    ) : (
                      "No logo"
                    )}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      color="primary"
                      onClick={() => handleEditManufacturer(manufacturer)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton
                      color="secondary"
                      onClick={() => handleDeleteManufacturer(manufacturer.id)}
                    >
                      <Delete />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ManufacturerTab;
