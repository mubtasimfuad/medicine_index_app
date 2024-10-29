// SearchBarComponent.tsx
import React, { useState, useEffect } from "react";
import { Box, TextField, Button, MenuItem } from "@mui/material";
import api from "../../services/api";

interface SearchBarProps {
  onSearch: (query: string, filters: any) => void;
}

const SearchBarComponent: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState<string>("");
  const [filters, setFilters] = useState<any>({
    category: "",
    form: "",
    manufacturer: "",
  });
  const [manufacturers, setManufacturers] = useState<
    { id: string; name: string }[]
  >([]);

  useEffect(() => {
    const fetchManufacturers = async () => {
      try {
        const response = await api.get("/manufacturers/"); // Ensure this endpoint returns a list of manufacturers with id and name
        setManufacturers(response.data.data || []);
      } catch (error) {
        console.error("Error fetching manufacturers:", error);
      }
    };

    fetchManufacturers();
  }, []);

  const handleSearch = () => {
    onSearch(query, filters);
  };

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFilters((prevFilters: any) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  return (
    <Box display="flex" flexDirection="column" gap={2} mb={3}>
      <TextField
        variant="outlined"
        placeholder="Search for medicines..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        fullWidth
      />

      <Box display="flex" gap={2}>
        <TextField
          select
          label="Category"
          name="category"
          value={filters.category}
          onChange={handleFilterChange}
          fullWidth
        >
          <MenuItem value="">All</MenuItem>
          <MenuItem value="ANT">Antibiotic</MenuItem>
          <MenuItem value="ANL">Analgesic</MenuItem>
          <MenuItem value="APR">Antipyretic</MenuItem>
          <MenuItem value="VIT">Vitamin</MenuItem>
          <MenuItem value="SUP">Supplement</MenuItem>
          <MenuItem value="OTH">Other</MenuItem>
        </TextField>

        <TextField
          select
          label="Form"
          name="form"
          value={filters.form}
          onChange={handleFilterChange}
          fullWidth
        >
          <MenuItem value="">All</MenuItem>
          <MenuItem value="TBL">Tablet</MenuItem>
          <MenuItem value="SYR">Syrup</MenuItem>
          <MenuItem value="INJ">Injection</MenuItem>
          <MenuItem value="ONT">Ointment</MenuItem>
          <MenuItem value="DRP">Drops</MenuItem>
          <MenuItem value="OTH">Other</MenuItem>
        </TextField>

        <TextField
          select
          label="Manufacturer"
          name="manufacturer"
          value={filters.manufacturer}
          onChange={handleFilterChange}
          fullWidth
        >
          <MenuItem value="">All</MenuItem>
          {manufacturers.map((manufacturer) => (
            <MenuItem key={manufacturer.id} value={manufacturer.id}>
              {manufacturer.name}
            </MenuItem>
          ))}
        </TextField>
      </Box>

      <Button variant="contained" color="primary" onClick={handleSearch}>
        Search
      </Button>
    </Box>
  );
};

export default SearchBarComponent;
