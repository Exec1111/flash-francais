import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardMedia,
  Grid,
  IconButton,
  Paper,
  Switch,
  Typography,
  FormControlLabel,
  CircularProgress,
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
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const navigate = useNavigate();
  const { user } = useAuth();

  // Fonction de chargement des ressources
  const fetchResources = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:10000/api/v1/resources', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setResources(data);
    } catch (error) {
      console.error('Erreur lors du chargement des ressources:', error);
      setResources([]);
    } finally {
      setLoading(false);
    }
  };

  // Fonctions de gestion des ressources
  const handleCreateResource = () => {
    navigate('/resources/new');
  };

  const handleEditResource = (id) => {
    navigate(`/resources/${id}/edit`);
  };

  const handleDeleteResource = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:10000/api/v1/resources/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // Recharger la liste après suppression
      fetchResources();
    } catch (error) {
      console.error('Erreur lors de la suppression de la ressource:', error);
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5" gutterBottom>
            Mes Ressources
          </Typography>
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
        </Box>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleCreateResource}
        >
          Nouvelle Ressource
        </Button>
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
                <CardMedia
                  component="img"
                  height="140"
                  image={resource.content?.url || '/placeholder.jpg'}
                  alt={resource.title}
                />
                <CardContent>
                  <Typography gutterBottom variant="h6" component="div">
                    {resource.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {resource.description}
                  </Typography>
                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="body2" color="primary">
                      {resource.type}
                    </Typography>
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
