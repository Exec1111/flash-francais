import React, { useState } from 'react';
import {
  Routes,
  Route,
  Navigate,
  Outlet,
  useNavigate,
  useLocation,
} from 'react-router-dom';
import { Box, Button, Typography } from '@mui/material'; 
import SideTreeView, { drawerWidth } from './components/SideTreeView';
import LandingPage from './pages/LandingPage';
import Login from './pages/auth/Login'; 
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import Dashboard from './pages/Dashboard';
import ResourceList from './components/resources/ResourceList';
import Contact from './pages/Contact';
import { useAuth } from './contexts/AuthContext';
import NewResource from './pages/resources/NewResource';
import ResourceEdit from './pages/resources/ResourceEdit';

// --- Composant de Layout Protégé ---
function ProtectedLayout() {
  const [open, setOpen] = useState(true); // Gère l'état du drawer

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* SideTreeView géré par le Layout */}
      <SideTreeView open={open} handleDrawerOpen={handleDrawerOpen} handleDrawerClose={handleDrawerClose} />

      {/* Contenu Principal */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          padding: 3,
          transition: (theme) => theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          marginLeft: `-${drawerWidth}px`, // Décale à gauche par défaut
          ...(open && { // Si le drawer est ouvert...
            transition: (theme) => theme.transitions.create('margin', {
              easing: theme.transitions.easing.easeOut,
              duration: theme.transitions.duration.enteringScreen,
            }),
            marginLeft: 0, // ...revient à sa position normale
          }),
        }}
      >
        {/* Barre d'application optionnelle (pour le bouton menu si drawer fermé) */}
        {/* Vous pouvez décommenter et styliser une AppBar si besoin */}
        {/**
        <AppBar position="fixed" sx={{ width: `calc(100% - ${open ? drawerWidth : 0}px)`, ml: `${open ? drawerWidth : 0}px`, transition: theme.transitions.create(['margin', 'width'], { easing: theme.transitions.easing.sharp, duration: theme.transitions.duration.leavingScreen }) }}>
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerOpen}
              edge="start"
              sx={{ mr: 2, ...(open && { display: 'none' }) }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap component="div">
              Flash Français
            </Typography>
          </Toolbar>
        </AppBar>
        <Toolbar /> // Pour l'espacement sous l'AppBar
        */}

        {/* C'est ici que le contenu de la page (DashboardPage) sera rendu */}
        <Outlet />
      </Box>
    </Box>
  );
}
// ---------------------------------

// --- Composant de Route Protégée ---
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) { 
    return <Navigate to="/login" replace />;
  }
  return children;
}
// ---------------------------------

function App() {
  const { isAuthenticated } = useAuth();
  console.log('App: État d\'authentification:', isAuthenticated);

  return (
    <Routes>
      {/* Routes publiques */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/auth/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Routes protégées */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <ProtectedLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
      </Route>

      <Route
        path="/resources"
        element={
          <ProtectedRoute>
            <ProtectedLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<ResourceList session={useAuth()} />} />
        <Route path="new" element={<NewResource />} />
        <Route path="edit/:id" element={<ResourceEdit />} />
      </Route>

      {/* Redirection par défaut */}
      <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/"} replace />} />
    </Routes>
  );
}

export default App;
