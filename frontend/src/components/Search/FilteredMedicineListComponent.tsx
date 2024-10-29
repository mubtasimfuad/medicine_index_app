// FilteredMedicineListComponent.tsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
} from "@mui/material";
import Pagination from "@mui/material/Pagination";
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
  generic_name_details: {
    name: string;
  };
  category_details: {
    name: string;
  };
  form_details: {
    form_type: string;
  };
  manufacturer_details: {
    name: string;
  };
  matches?: {
    name: [number, number][];
    generic_name: [number, number][];
  };
}

interface FilteredMedicineListProps {
  query: string;
  filters: any;
}

const FilteredMedicineListComponent: React.FC<FilteredMedicineListProps> = ({
  query,
  filters,
}) => {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [page, setPage] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (query) {
      fetchSearchResults();
    }
  }, [query, filters, page]);

  const fetchSearchResults = async () => {
    setLoading(true);

    try {
      const activeFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value)
      );

      const params = {
        q: query,
        page,
        ...(Object.keys(activeFilters).length > 0 && {
          filters: JSON.stringify(activeFilters),
        }),
      };

      const response = await api.get("/medicines/search/", { params });
      const { results, count } = response.data;

      setMedicines(results || []);
      setTotalPages(Math.ceil(count / 10));
    } catch (error) {
      console.error("Error fetching search results:", error);
      setMedicines([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  const applyHighlight = (text: string, matches: [number, number][]) => {
    if (!matches || matches.length === 0) return text;

    const highlightedText = [];
    let lastIndex = 0;

    matches.forEach(([start, end], index) => {
      highlightedText.push(text.slice(lastIndex, start));
      highlightedText.push(
        <span key={`highlight-${index}`} style={{ backgroundColor: "yellow" }}>
          {text.slice(start, end)}
        </span>
      );
      lastIndex = end;
    });

    highlightedText.push(text.slice(lastIndex));
    return highlightedText;
  };

  return (
    <Box mt={4}>
      {loading ? (
        <Typography variant="h6">Loading...</Typography>
      ) : medicines.length === 0 ? (
        <Typography variant="h6">No results found.</Typography>
      ) : (
        <>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Price</TableCell>
                  <TableCell>Generic Name</TableCell>
                  <TableCell>Category</TableCell>
                  <TableCell>Form</TableCell>
                  <TableCell>Manufacturer</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {medicines.map((medicine) => (
                  <TableRow key={medicine.id}>
                    <TableCell>
                      {medicine.matches?.name
                        ? applyHighlight(medicine.name, medicine.matches.name)
                        : medicine.name}
                    </TableCell>
                    <TableCell>{medicine.description}</TableCell>
                    <TableCell>{medicine.price}</TableCell>
                    <TableCell>
                      {medicine.matches?.generic_name
                        ? applyHighlight(
                            medicine.generic_name_details?.name,
                            medicine.matches.generic_name
                          )
                        : medicine.generic_name_details?.name}
                    </TableCell>
                    <TableCell>{medicine.category_details?.name}</TableCell>
                    <TableCell>{medicine.form_details?.form_type}</TableCell>
                    <TableCell>{medicine.manufacturer_details?.name}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          {/* Pagination Controls */}
          <Box display="flex" justifyContent="center" mt={2}>
            <Pagination
              count={totalPages}
              page={page}
              onChange={handlePageChange}
            />
          </Box>
        </>
      )}
    </Box>
  );
};

export default FilteredMedicineListComponent;
