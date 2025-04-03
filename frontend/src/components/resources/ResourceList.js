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
        <IconButton size="small" title="Modifier">
          <EditIcon />
        </IconButton>
        <IconButton size="small" title="Supprimer" color="error">
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

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const response = await fetch('/api/resources');
      const data = await response.json();
      setResources(data);
    } catch (error) {
      console.error('Erreur lors du chargement des ressources:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateResource = () => {
    navigate('/resources/new');
  };

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
                      <IconButton size="small" title="Modifier">
                        <EditIcon />
                      </IconButton>
                      <IconButton size="small" title="Supprimer" color="error">
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
