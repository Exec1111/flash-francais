import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  IconButton,
  Alert,
  Paper,
  CircularProgress,
  FormControlLabel,
  Switch,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { DataGrid } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const columns = [
  { field: 'id', headerName: 'ID', width: 90 },
  { field: 'title', headerName: 'Titre', width: 200 },
  { 
    field: 'type', 
    headerName: 'Type', 
    width: 130,
    valueFormatter: (params) => params.value.charAt(0).toUpperCase() + params.value.slice(1)
  },
  { 
    field: 'description', 
    headerName: 'Description', 
    width: 300,
    flex: 1 
  },
  { 
    field: 'actions', 
    headerName: 'Actions', 
    width: 130,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', gap: 1 }}>
        <IconButton size="small" title="Modifier" data-action="edit">
          <EditIcon />
        </IconButton>
        <IconButton size="small" title="Supprimer" color="error" data-action="delete">
          <DeleteIcon />
        </IconButton>
      </Box>
    )
  }
];

const ResourceList = () => {
  const { user } = useAuth();
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const navigate = useNavigate();

  // Fonction de chargement des ressources
  const fetchResources = async () => {
    try {
      const response = await fetch('http://localhost:10000/api/v1/resources', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Erreur lors du chargement des ressources');
      }

      const data = await response.json();
      setResources(data);
    } catch (err) {
      console.error('Erreur lors du chargement des ressources:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fonctions de gestion des ressources
  const handleCreateResource = () => {
    console.log('ResourceList: Début de la création de ressource');
    
    // Récupérer les données utilisateur depuis le localStorage
    const user = localStorage.getItem('user');
    console.log('ResourceList: Données brutes du localStorage:', user);
    
    const userData = user ? JSON.parse(user) : null;
    console.log('ResourceList: Données utilisateur après parsing:', userData);
    
    const userId = userData?.id;
    console.log('ResourceList: ID de l\'utilisateur trouvé:', userId);

    if (!userId) {
      console.error('ResourceList: ID utilisateur non défini');
      return;
    }

    // Redirection vers la page de création avec l'ID de l'utilisateur
    navigate(`/resources/new?userId=${userId}`);
    console.log('ResourceList: Redirection vers /resources/new avec userId:', userId);
  };

  const handleEditResource = (id) => {
    navigate(`/resources/${id}/edit`);
  };

  const handleDeleteResource = async (id) => {
    try {
      const response = await fetch(`http://localhost:10000/api/v1/resources/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la suppression de la ressource');
      }

      // Recharger la liste après suppression
      fetchResources();
    } catch (err) {
      console.error('Erreur lors de la suppression de la ressource:', err);
    }
  };

  // Effet de chargement initial
  useEffect(() => {
    fetchResources();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', pt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Typography variant="h6" component="h2">
              Mes Ressources
            </Typography>
          </Grid>
          <Grid item xs="auto">
            <Button
              variant="contained"
              color="primary"
              startIcon={<AddIcon />}
              onClick={handleCreateResource}
            >
              Nouvelle ressource
            </Button>
          </Grid>
          <Grid item xs="auto">
            <FormControlLabel
              control={
                <Switch
                  checked={viewMode === 'table'}
                  onChange={(e) => setViewMode(e.target.checked ? 'table' : 'grid')}
                  name="viewMode"
                />
              }
              label="Vue Table"
            />
          </Grid>
        </Grid>
      </Box>

      {viewMode === 'table' ? (
        <Paper sx={{ width: '100%', mb: 2 }}>
          <DataGrid
            rows={resources}
            columns={columns}
            pageSize={10}
            rowsPerPageOptions={[10]}
            checkboxSelection
            disableSelectionOnClick
            autoHeight
            onCellClick={(params, event) => {
              if (params.field === 'actions') {
                if (event.target.closest('button')) {
                  const action = event.target.closest('button').dataset.action;
                  if (action === 'edit') {
                    handleEditResource(params.id);
                  } else if (action === 'delete') {
                    handleDeleteResource(params.id);
                  }
                }
              }
            }}
          />
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {resources.map((resource) => (
            <Grid item xs={12} sm={6} md={4} key={resource.id}>
              <Card>
                <CardHeader
                  title={resource.title}
                  subheader={resource.description}
                />
                <CardContent>
                  <Typography variant="body2" color="text.secondary">
                    Type: {resource.type}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {typeof resource.content === 'object' ? 
                      (resource.content.url ? resource.content.url : JSON.stringify(resource.content)) :
                      resource.content}
                  </Typography>
                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton 
                        size="small" 
                        title="Modifier" 
                        data-action="edit"
                        onClick={() => handleEditResource(resource.id)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton 
                        size="small" 
                        title="Supprimer" 
                        color="error"
                        data-action="delete"
                        onClick={() => handleDeleteResource(resource.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default ResourceList;
