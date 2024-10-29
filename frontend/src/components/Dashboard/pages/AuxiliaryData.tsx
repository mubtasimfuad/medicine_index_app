import React, { useState } from 'react';
import { Box, Tabs, Tab, Typography, Container } from '@mui/material';
import CategoryTab from './Auxiliary/CategoryTab';  // Updated relative path
import FormTab from './Auxiliary/FormTab';
import GenericNameTab from './Auxiliary/GenericNameTab';
import ManufacturerTab from './Auxiliary/ManufacturerTab';

const AuxiliaryData: React.FC = () => {
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Manage Auxiliary Data
      </Typography>
      <Tabs value={currentTab} onChange={handleTabChange} indicatorColor="primary" textColor="primary">
        <Tab label="Categories" />
        <Tab label="Forms" />
        <Tab label="Generic Names" />
        <Tab label="Manufacturers" />
      </Tabs>
      <Box mt={3}>
        {currentTab === 0 && <CategoryTab />}
        {currentTab === 1 && <FormTab />}
        {currentTab === 2 && <GenericNameTab />}
        {currentTab === 3 && <ManufacturerTab />}
      </Box>
    </Container>
  );
};

export default AuxiliaryData;
