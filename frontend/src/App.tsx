// src/App.tsx

import React from 'react';
import { Button, Container, Typography, TextField, Card, CardContent, Box, Grid } from '@mui/material';

const App: React.FC = () => {
  return (
    <Container maxWidth="md" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center' }}>
      <Box width="100%">
        <Grid container spacing={3} direction="column" alignItems="center" justifyContent="center">
          <Grid item xs={12}>
            <Typography variant="h1" align="center" gutterBottom>
              Medicine Index
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1" align="center" gutterBottom>
              Welcome to the Medicine Index Application! Here, you can search, view, and manage medicines.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={8}>
            <TextField
              label="Search Medicines"
              variant="outlined"
              fullWidth
              margin="normal"
            />
          </Grid>
          <Grid item xs={12} sm={8}>
            <Button variant="contained" color="primary" fullWidth>
              Search
            </Button>
          </Grid>
          <Grid item xs={12} sm={8}>
            <Card>
              <CardContent>
                <Typography variant="h3" color="textPrimary" align="center">
                  Sample Card
                </Typography>
                <Typography variant="body2" color="textSecondary" align="center">
                  The boilerplate code for the Medicine Index application is ready.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default App;
