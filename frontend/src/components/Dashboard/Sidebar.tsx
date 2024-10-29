// Sidebar.tsx
import React from "react";
import { List, ListItem, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { SidebarContainer } from "./Dashboard.styles";

const Sidebar: React.FC = () => (
  <SidebarContainer>
    <Typography variant="h5" gutterBottom>
      Admin Dashboard
    </Typography>
    <List>
      <ListItem>
        <Button component={Link} to="/dashboard/medicine-list" fullWidth>
          Medicine List
        </Button>
      </ListItem>
      <ListItem>
        <Button component={Link} to="/dashboard/add-medicine" fullWidth>
          Add Medicine
        </Button>
      </ListItem>
      <ListItem>
        <Button component={Link} to="/dashboard/auxiliary-data" fullWidth>
          Auxiliary Data
        </Button>
      </ListItem>
    </List>
  </SidebarContainer>
);

export default Sidebar;
