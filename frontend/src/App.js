import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import Dashboard from './pages/Dashboard';
import authService from './services/auth';

// Composant pour les routes protégées
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Composant pour les routes publiques (accessibles uniquement si non connecté)
const PublicRoute = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();
  const location = useLocation();
  
  if (isAuthenticated && location.pathname !== '/') {
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Fonction de déconnexion
  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          // Vérifier si le token est toujours valide
          await authService.getCurrentUser();
        }
      } catch (error) {
        // Si le token n'est plus valide, déconnecter l'utilisateur
        authService.logout();
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Afficher un écran de chargement pendant la vérification de l'authentification
  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        Chargement...
      </div>
    );
  }

  return (
    <Routes>
      {/* Routes publiques */}
      <Route path="/" element={<PublicRoute><LandingPage /></PublicRoute>} />
      <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
      <Route path="/forgot-password" element={<PublicRoute><ForgotPassword /></PublicRoute>} />
      
      {/* Routes protégées */}
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard onLogout={handleLogout} /></ProtectedRoute>} />
      
      {/* Redirection par défaut */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
