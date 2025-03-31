import React from 'react';
import {
  Box,
  Typography,
  Button,
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Avatar,
  Grid,
  Card,
  CardContent,
  CardActions,
  Divider,
  useTheme
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AddIcon from '@mui/icons-material/Add';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import BarChartIcon from '@mui/icons-material/BarChart';
import PeopleIcon from '@mui/icons-material/People';

const Dashboard = ({ onLogout }) => {
  const theme = useTheme();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid rgba(255, 255, 255, 0.12)' }}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              flexGrow: 1,
              fontWeight: 700,
              background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              color: 'transparent'
            }}
          >
            Flash Français
          </Typography>
          <Button color="inherit" onClick={onLogout}>Déconnexion</Button>
          <Avatar sx={{ ml: 2, bgcolor: theme.palette.primary.main }}>P</Avatar>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" component="h1" fontWeight={700}>
            Bonjour, Professeur
          </Typography>
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<AddIcon />}
          >
            Nouvelle progression
          </Button>
        </Box>

        <Grid container spacing={3}>
          {/* Statistiques */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center',
                      width: 40, 
                      height: 40, 
                      borderRadius: '50%', 
                      backgroundColor: 'rgba(79, 106, 255, 0.1)',
                      mr: 2
                    }}
                  >
                    <AutoStoriesIcon sx={{ color: theme.palette.primary.main }} />
                  </Box>
                  <Typography variant="h6" component="h2">
                    Flashcards
                  </Typography>
                </Box>
                <Typography variant="h3" component="p" fontWeight={700}>
                  124
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Flashcards créées
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center',
                      width: 40, 
                      height: 40, 
                      borderRadius: '50%', 
                      backgroundColor: 'rgba(255, 79, 106, 0.1)',
                      mr: 2
                    }}
                  >
                    <PeopleIcon sx={{ color: theme.palette.secondary.main }} />
                  </Box>
                  <Typography variant="h6" component="h2">
                    Élèves
                  </Typography>
                </Box>
                <Typography variant="h3" component="p" fontWeight={700}>
                  48
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Élèves actifs
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center',
                      width: 40, 
                      height: 40, 
                      borderRadius: '50%', 
                      backgroundColor: 'rgba(102, 187, 106, 0.1)',
                      mr: 2
                    }}
                  >
                    <BarChartIcon sx={{ color: theme.palette.success.main }} />
                  </Box>
                  <Typography variant="h6" component="h2">
                    Progression
                  </Typography>
                </Box>
                <Typography variant="h3" component="p" fontWeight={700}>
                  78%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Taux de réussite moyen
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Progressions récentes */}
          <Grid item xs={12}>
            <Typography variant="h5" component="h2" sx={{ mb: 2, mt: 2 }}>
              Progressions récentes
            </Typography>
            <Divider sx={{ mb: 3 }} />
            
            <Grid container spacing={3}>
              {[
                { title: "Vocabulaire de base", count: 32, level: "A1", color: theme.palette.primary.main },
                { title: "Expressions idiomatiques", count: 45, level: "B1", color: theme.palette.secondary.main },
                { title: "Grammaire avancée", count: 28, level: "C1", color: theme.palette.success.main },
                { title: "Conjugaison", count: 19, level: "A2", color: theme.palette.warning.main }
              ].map((progression, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Box 
                        sx={{ 
                          display: 'inline-block',
                          px: 1.5,
                          py: 0.5,
                          borderRadius: 1,
                          backgroundColor: `${progression.color}20`,
                          color: progression.color,
                          fontWeight: 600,
                          fontSize: '0.75rem',
                          mb: 2
                        }}
                      >
                        Niveau {progression.level}
                      </Box>
                      <Typography variant="h6" component="h3" gutterBottom>
                        {progression.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {progression.count} flashcards
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" color="primary">
                        Modifier
                      </Button>
                      <Button size="small" color="primary">
                        Voir
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard;
