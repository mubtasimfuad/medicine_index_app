import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute: React.FC = () => {
  const isAuthenticated = Boolean(localStorage.getItem('authToken')); // Adjust based on your authentication setup

  return isAuthenticated ? <Outlet /> : <Outlet /> ;
};

export default ProtectedRoute;
