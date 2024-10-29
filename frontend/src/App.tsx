// App.tsx
import { Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "./components/Dashboard/Dashboard";
import MedicineList from "./components/Dashboard/pages/MedicineListAdmin";
import AddMedicine from "./components/Dashboard/pages/AddMedicine";
import AuxiliaryData from "./components/Dashboard/pages/AuxiliaryData";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./components/Login/Login";
import Navbar from "./components/Navbar";
import { AuthProvider } from "./services/AuthContext"; // Import AuthProvider

function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        {/* Protected Dashboard Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />}>
            <Route index element={<Navigate to="medicine-list" replace />} />
            <Route path="medicine-list" element={<MedicineList />} />
            <Route path="add-medicine" element={<AddMedicine />} />
            <Route path="auxiliary-data" element={<AuxiliaryData />} />
          </Route>
        </Route>
      </Routes>
    </AuthProvider>
  );
}

export default App;
