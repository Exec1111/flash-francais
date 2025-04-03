import React, { useState } from 'react';
import {
  Routes,
  Route,
  Navigate,
  Outlet,
  useNavigate, // Importer useNavigate
} from 'react-router-dom';
import { Box, Button, Typography, AppBar, Toolbar, IconButton } from '@mui/material'; 
import { Menu as MenuIcon } from '@mui/icons-material'; // Importer MenuIcon pour l'AppBar
import theme from './theme'; // Garder l'import de theme s'il est utilisé ailleurs
import SideTreeView, { drawerWidth } from './components/SideTreeView'; // Importer drawerWidth
import LandingPage from './pages/LandingPage';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import Dashboard from './pages/Dashboard';
import authService from './services/auth';

// --- Simulation simple de l'authentification ---
let authStatus = false; // Remplacez par votre logique d'auth réelle
const login = () => { authStatus = true; };
const logout = () => { authStatus = false; };
const isAuthenticated = () => authStatus;
// ----------------------------------------------

// --- Composants de page simples ---
function LoginPage() {
  const navigate = useNavigate(); // Obtenir la fonction de navigation
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <Typography variant="h4">Page de Login</Typography>
      {/* Utiliser navigate au lieu de window.location.href */}
      <Button variant="contained" onClick={() => { login(); navigate('/dashboard'); }}>Se connecter (Simulation)</Button>
    </Box>
  );
}

function DashboardPage() {
  const navigate = useNavigate(); // Ajouter aussi ici pour le bouton logout
  return (
    <Box>
      <Typography variant="h4">Tableau de Bord</Typography>
      <Typography>Contenu principal du tableau de bord...</Typography>
      {/* Les autres composants du dashboard viendront ici */}
      {/* Utiliser navigate aussi pour la déconnexion simulée */}
      <Button variant="outlined" onClick={() => { logout(); navigate('/login'); }}>Se déconnecter</Button>
    </Box>
  );
}
// ---------------------------------

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
        {/*
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
  // Utiliser la fonction de simulation isAuthenticated pour la cohérence
  if (!isAuthenticated()) { 
    // Redirige vers la page de login si non authentifié
    return <Navigate to="/login" replace />;
  }
  return children;
}
// ---------------------------------

function App() {
  return (
    <Routes>
      {/* Route pour la page publique LandingPage (exemple) */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Routes protégées utilisant le ProtectedLayout */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <ProtectedLayout />
          </ProtectedRoute>
        }
      >
         {/* Route enfant pour le contenu du Dashboard */}
        <Route index element={<Dashboard />} />
         {/* Ajoutez d'autres routes enfants du dashboard ici si nécessaire */}
         {/* exemple: <Route path="settings" element={<SettingsPage />} /> */}
      </Route>

      {/* Redirection par défaut */}
      {/* Utiliser la fonction de simulation isAuthenticated ici aussi */}
      <Route path="*" element={<Navigate to={isAuthenticated() ? "/dashboard" : "/login"} replace />} />
    </Routes>
  );
}

export default App;
