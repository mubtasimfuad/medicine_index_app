import React from 'react';
import { Typography } from '@mui/material';
import { ContentContainer } from './Dashboard.styles';

const Content: React.FC = () => {
  return (
    <ContentContainer>
      <Typography variant="h4" gutterBottom>
        Welcome to the Admin Dashboard
      </Typography>
      <Typography variant="body1">
        Select an option from the sidebar to manage medicines and auxiliary data.
      </Typography>
    </ContentContainer>
  );
};

export default Content;
