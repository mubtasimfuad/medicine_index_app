// src/pages/SearchView.tsx
import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  CircularProgress,
  List,
  ListItem,
} from "@mui/material";
import { searchMedicines } from "../services/api";

interface Match {
  start: number;
  end: number;
}

interface Medicine {
  id: string;
  name: string;
  description: string;
  matches: {
    name: Match[];
    generic_name: Match[];
  };
}

const SearchView: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const results = await searchMedicines(query);
      setMedicines(results);
    } catch (error) {
      console.error("Error fetching search results:", error);
    } finally {
      setLoading(false);
    }
  };

  const highlightText = (text: string, matches: Match[]) => {
    let highlightedText = [];
    let lastIndex = 0;

    matches.forEach((match, index) => {
      highlightedText.push(text.slice(lastIndex, match.start)); // Text before match
      highlightedText.push(
        <span key={index} style={{ backgroundColor: "yellow" }}>
          {text.slice(match.start, match.end)}
        </span>
      );
      lastIndex = match.end;
    });

    highlightedText.push(text.slice(lastIndex)); // Remaining text after the last match
    return highlightedText;
  };

  return (
    <Box sx={{ padding: 3 }}>
      <Typography variant="h4" gutterBottom>
        Search Medicines
      </Typography>
      <Box display="flex" gap={2}>
        <TextField
          variant="outlined"
          fullWidth
          label="Search by name or generic name"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button variant="contained" onClick={handleSearch}>
          Search
        </Button>
      </Box>
      {loading && <CircularProgress />}
      <List>
        {medicines.map((medicine) => (
          <ListItem key={medicine.id}>
            <Box>
              <Typography variant="h6">
                {highlightText(medicine.name, medicine.matches.name)}
              </Typography>
              <Typography variant="body2">
                {highlightText(
                  medicine.description,
                  medicine.matches.generic_name
                )}
              </Typography>
            </Box>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default SearchView;
