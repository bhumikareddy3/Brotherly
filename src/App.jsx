import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AppProvider } from "./context/AppContext";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/Home";
import Assessment from "./pages/Assessment";
import Mentor from "./pages/Mentor";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Conversations from "./pages/Conversations";
import Login from "./pages/Login";
import Register from "./pages/Register";

export default function App() {
  return (
    <AuthProvider>
      <AppProvider>
        <BrowserRouter>
          <Routes>
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />

            <Route
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Home />} />
              <Route path="assessment" element={<Assessment />} />
              <Route path="mentor" element={<Mentor />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="history" element={<History />} />
              <Route path="conversations" element={<Conversations />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </AuthProvider>
  );
}
