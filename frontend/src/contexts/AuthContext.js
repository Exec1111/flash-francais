import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      console.log('AuthProvider: Vérification de l\'authentification');
      try {
        const token = localStorage.getItem('token');
        console.log('AuthProvider: Token trouvé:', !!token);
        if (token) {
          const response = await fetch('http://localhost:10000/api/v1/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
          
          if (response.ok) {
            const userData = await response.json();
            console.log('AuthProvider: Utilisateur authentifié:', userData);
            setUser(userData);
            setIsAuthenticated(true);
          } else {
            console.log('AuthProvider: Token invalide, nettoyage');
            localStorage.removeItem('token');
            localStorage.removeItem('user');
          }
        }
      } catch (error) {
        console.error('AuthProvider: Erreur lors de la vérification:', error);
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      console.log('AuthProvider: Tentative de connexion');
      const userData = await authService.login(email, password);
      console.log('AuthProvider: Connexion réussie, mise à jour du contexte');
      setUser(userData);
      setIsAuthenticated(true);
      // Ne pas rediriger ici, c'est le composant Login qui s'en charge
    } catch (error) {
      console.error('AuthProvider: Erreur lors de la connexion:', error);
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      user,
      loading,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error('useAuth doit être utilisé dans un AuthProvider');
  }
  return context;
};
