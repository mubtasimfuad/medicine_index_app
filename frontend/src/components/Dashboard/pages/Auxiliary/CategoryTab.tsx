import React, { useState, useEffect } from 'react';
import { Box, Button, TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';
import api from '../../../../services/api';

interface Category {
  id: number;
  name: string;
}

const CategoryTab: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [categoryName, setCategoryName] = useState('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get('/categories/');
        setCategories(response.data.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  const handleAddCategory = async () => {
    try {
      const response = await api.post('/categories/', { name: categoryName });
      setCategories([...categories, response.data.data]);
      setCategoryName('');
    } catch (error) {
      console.error('Error adding category:', error);
    }
  };

  const handleDeleteCategory = async (id: number) => {
    try {
      await api.delete(`/categories/${id}/`);
      setCategories(categories.filter((category) => category.id !== id));
    } catch (error) {
      console.error('Error deleting category:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Manage Categories
      </Typography>
      
      {/* Responsive form container */}
      <Box 
        display="flex" 
        alignItems="center" 
        gap={2} 
        flexWrap="wrap" 
        sx={{ mt: 2, mb: 3 }}
      >
        <TextField
          label="Category Name"
          value={categoryName}
          onChange={(e) => setCategoryName(e.target.value)}
          margin="normal"
          fullWidth={false}
          sx={{ flexGrow: 1, minWidth: '200px' }}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleAddCategory}
          sx={{ minWidth: '120px' }}
        >
          Add Category
        </Button>
      </Box>

      {/* Responsive table container */}
      <TableContainer component={Paper} sx={{ overflowX: 'auto', mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {categories.map((category) => (
              <TableRow key={category.id}>
                <TableCell>{category.name}</TableCell>
                <TableCell>
                  <Button 
                    color="secondary" 
                    onClick={() => handleDeleteCategory(category.id)}
                  >
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

export default CategoryTab;
