// Dashboard.tsx
import React from "react";
import { Box, Grid } from "@mui/material";
import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";

const Dashboard: React.FC = () => {
  return (
    <Grid container>
      {/* Sidebar */}
      <Grid item xs={3}>
        <Sidebar />
      </Grid>

      {/* Main Content */}
      <Grid item xs={9}>
        <Box padding={3}>
          <Outlet /> {/* This will render the nested route components */}
        </Box>
      </Grid>
    </Grid>
  );
};

export default Dashboard;
