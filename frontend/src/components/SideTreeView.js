import React, { useRef, useState, useEffect } from 'react';
import { Drawer, IconButton, Box, Typography, useTheme, Tooltip, CircularProgress, Divider } from '@mui/material';
import { 
  Menu as MenuIcon,
  ChevronLeft as ChevronLeftIcon, 
  Description as DescriptionIcon, 
  Checklist as ChecklistIcon,
  AccountTree as AccountTreeIcon,
  FormatListBulleted as FormatListBulletedIcon,
  Folder as FolderIcon, 
  Article as ArticleIcon, 
  OndemandVideo as VideoIcon, 
  FitnessCenter as ExerciseIcon 
} from '@mui/icons-material';
import { SimpleTreeView, TreeItem } from '@mui/x-tree-view'; 
import ResourceButton from './resources/ResourceButton';

export const drawerWidth = 480;  

function SideTreeView({ open, handleDrawerOpen, handleDrawerClose }) {
  const theme = useTheme();
  const [treeData, setTreeData] = useState({ id: 'root', name: 'Progressions', type: 'root', children: [] }); 
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const textRef = useRef(null);
  const [isTextTruncated, setIsTextTruncated] = useState(false);
  const [expandedItems, setExpandedItems] = useState([]); 

  const checkTextTruncation = React.useCallback(() => {
    if (textRef.current) {
      const isOverflowing = textRef.current.scrollWidth > textRef.current.clientWidth;
      setIsTextTruncated(isOverflowing);
    }
  }, []);

  useEffect(() => {
    checkTextTruncation();
    const resizeObserver = new ResizeObserver(checkTextTruncation);
    if (textRef.current) {
      resizeObserver.observe(textRef.current);
    }
    return () => resizeObserver.disconnect();
  }, [checkTextTruncation]);

  const findAndUpdateNodeImmutable = (nodes, nodeId, newChildren) => {
    return nodes.map(node => {
      if (node.id.toString() === nodeId.toString()) {
        console.log(`Updating children for node ${nodeId} immutably.`); 
        return { ...node, children: newChildren };
      } else if (node.children && node.children.length > 0) {
        const updatedChildren = findAndUpdateNodeImmutable(node.children, nodeId, newChildren);
        if (updatedChildren !== node.children) {
          return { ...node, children: updatedChildren };
        }
      }
      return node;
    });
  };

  const updateNodeChildrenImmutable = (nodeId, newChildren) => {
    setTreeData(prevData => {
      console.log(`Calling setTreeData after immutable update for ${nodeId}`);
      const updatedRootChildren = findAndUpdateNodeImmutable(prevData.children, nodeId, newChildren);
      if (updatedRootChildren !== prevData.children) {
        return { ...prevData, children: updatedRootChildren };
      } else {
        console.warn(`Node ${nodeId} not found or no change detected for immutable update.`);
        return prevData;
      }
    });
  };  

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch('http://localhost:10000/api/v1/progressions'); 
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const progressions = await response.json();
        // Adapter les données reçues au format attendu par renderTree
        const formattedProgressions = progressions.map(prog => ({
          id: prog.id,
          name: prog.title, 
          type: 'progression', 
          description: prog.description, // Garder la description si besoin ailleurs
          // Ajouter un enfant factice pour que l'icône d'expansion s'affiche
          children: [{ id: `loading-${prog.id}`, name: 'Chargement...', type: 'loading' }] // Dummy child for sessions
        }));

        console.log("Données formatées pour TreeView:", formattedProgressions);
        setTreeData(prevData => ({ ...prevData, children: formattedProgressions }));
      } catch (e) {
        console.error("Erreur lors de la récupération des données de l'API:", e);
        setError('Impossible de charger les progressions.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []); 

  const renderedTreeNodes = React.useMemo(() => {
    // Helper function to render the tree recursively
    const renderTree = (nodes, currentExpandedItems) =>
      // Vérifier si nodes est bien un tableau avant de mapper
      Array.isArray(nodes) && nodes.map((node) => (
        <TreeItem
          key={node.id} // React key
          itemId={node.id.toString()} // Ensure itemId is a string
          // sx prop removed to show expand/collapse icons
          label={(
            <Box 
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between', // Rétablir l'alignement horizontal
                width: '100%', 
                p: 1, 
                overflow: 'hidden', 
              }}
            >
              <Tooltip 
                title={isTextTruncated ? node.name : ""} // Only show tooltip if truncated
                placement="bottom-start"
              >
                <Box 
                  sx={{
                    flexGrow: 1,
                    overflow: 'hidden',
                  }}
                  ref={textRef} // Attach ref to the box containing the text
                  onMouseEnter={checkTextTruncation} // Check truncation on hover
                  onMouseLeave={() => setIsTextTruncated(false)} // Reset on leave
                > 
                  <Typography
                    variant="body2"
                    sx={{
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                    }}
                  >
                    {node.name}
                  </Typography>
                </Box>
              </Tooltip>
              {/* Icônes spécifiques au type de noeud */}
              <Box sx={{ display: 'flex', alignItems: 'center', ml: 1 }}> {/* Container for icons */} 
                {node.type === 'progression' && (
                  <FolderIcon sx={{ fontSize: 18, color: 'action.active' }} /> 
                )}
                {/* Icône Objectifs pour les séquences AVEC objectifs */} 
                {node.type === 'sequence' && Array.isArray(node.objectives) && node.objectives.length > 0 && (
                  <Tooltip 
                    placement="right"
                    title={(
                      <Box sx={{ p: 1 }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>Objectifs :</Typography>
                        {node.objectives.map((obj, index) => (
                          // Utiliser un Tooltip interne pour la description de chaque objectif
                          <Tooltip key={`obj-tooltip-${node.id}-${index}`} title={obj.description || ''} placement="top-start">
                            <Typography variant="body2" sx={{ mb: 0.5 }}>
                              - {obj.title}
                            </Typography>
                          </Tooltip>
                        ))}
                      </Box>
                    )}
                  >
                    {/* L'icône elle-même */} 
                    <ChecklistIcon sx={{ fontSize: 18, color: 'primary.main', ml: 0.5 }} />
                  </Tooltip>
                )}
                {node.type === 'sequence' && (
                  <AccountTreeIcon sx={{ fontSize: 18, color: 'action.active' }} />
                )}
                {node.type === 'seance' && (
                  <FormatListBulletedIcon sx={{ fontSize: 18, color: 'action.active' }} />
                )}
                {/* Icône pour les ressources - spécifique au type */}
                {node.type === 'resource' && (
                  (() => {
                    console.log(`Resource Node: ${node.name}, Type:`, node.resource_type); // DEBUG LOG
                    const iconProps = { sx: { fontSize: 18, color: 'action.active' } };
                    switch (node.resource_type?.toLowerCase()) {
                      case 'text':
                        return <DescriptionIcon {...iconProps} />;
                      case 'video':
                        return <VideoIcon {...iconProps} />;
                      case 'exercise':
                        return <ExerciseIcon {...iconProps} />;
                      // Add other cases like 'link', 'pdf' if needed
                      default:
                        return <ArticleIcon {...iconProps} />; // Default icon
                    }
                  })()
                )}
                {/* Ne pas afficher d'icône pour le type 'loading' ou 'error' */} 
              </Box>
            </Box>
          )}
        >
          {/* Les enfants directs du TreeItem (loading ou enfants récursifs) */} 
          {/* Affichage conditionnel pendant le chargement ou pour les enfants normaux */}
          {Array.isArray(node.children) && node.children.length > 0 ? (
            // Afficher un indicateur de chargement si l'enfant est le noeud factice
            node.children.length === 1 && node.children[0].type === 'loading' ? (
              <Box sx={{ display: 'flex', alignItems: 'center', pl: 4, pt: 1, color: 'text.secondary' }}>
                <CircularProgress size={16} sx={{ mr: 1 }} />
                <Typography variant="caption">{node.children[0].name}</Typography>
              </Box>
            ) : (
              // Sinon, rendre les enfants récursivement
              renderTree(node.children, currentExpandedItems)
            )
          ) : null}
        {/* Fin des enfants directs */} 
 
        </TreeItem>
      ));
    // Fin de renderTree

    // Appel initial pour les enfants directs de treeData
    return renderTree(treeData.children, expandedItems); // Passer expandedItems ici
 
  }, [treeData, isTextTruncated, textRef, checkTextTruncation, expandedItems]); // Ajout de expandedItems aux dépendances

  const handleExpandedItemsChange = (event, itemIds) => {
    console.log("Expanded items changed:", itemIds); // LOG 1
    setExpandedItems(itemIds); // Update the expanded state

    // Find the node that was just expanded
    const newlyExpandedItemId = itemIds.find(id => !expandedItems.includes(id));
    console.log("Newly expanded item ID:", newlyExpandedItemId); // LOG 2

    if (!newlyExpandedItemId) {
      return; // No item was newly expanded (likely a collapse)
    }

    // Find the corresponding node in the tree data
    let nodeToExpand = null;
    const findNode = (nodes) => {
      for (const node of nodes) {
        if (node.id.toString() === newlyExpandedItemId.toString()) {
          nodeToExpand = node;
          return;
        }
        if (node.children && node.children.length > 0) {
          findNode(node.children);
          if (nodeToExpand) return; 
        }
      }
    };
    findNode(treeData.children);

    console.log(`Vérification pour nodeId: ${newlyExpandedItemId}`, nodeToExpand); // LOG 3

    // --- LOAD SEQUENCES --- 
    if (nodeToExpand && nodeToExpand.type === 'progression' && nodeToExpand.children.length === 1 && nodeToExpand.children[0].type === 'loading') {
      console.log(`CONDITION REMPLIE pour PROGRESSION ${newlyExpandedItemId}. Chargement des séquences...`); // LOG 4
      (async () => {
        try {
          const response = await fetch(`http://localhost:10000/api/v1/sequences/by_progression/${newlyExpandedItemId}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const sequences = await response.json();
          console.log(`Séquences reçues pour progression ${newlyExpandedItemId}:`, sequences);

          const formattedSequences = sequences.map(seq => ({
            id: seq.id,
            name: seq.title,
            type: 'sequence',
            description: seq.description,
            objectives: seq.objectives || [], 
            children: [{ id: `loading-seq-${seq.id}`, name: 'Chargement sessions...', type: 'loading' }] // Dummy child for sessions
          }));

          updateNodeChildrenImmutable(newlyExpandedItemId, formattedSequences);

        } catch (error) {
          console.error("Erreur lors du chargement des séquences:", error);
          updateNodeChildrenImmutable(newlyExpandedItemId, [{ id: `error-seq-${newlyExpandedItemId}`, name: 'Erreur chargement séquences', type: 'error' }]);
        }
      })();
    } 
    // --- LOAD SESSIONS --- 
    else if (nodeToExpand && nodeToExpand.type === 'sequence' && nodeToExpand.children.length === 1 && nodeToExpand.children[0].type === 'loading') {
      console.log(`CONDITION REMPLIE pour SÉQUENCE ${newlyExpandedItemId}. Chargement des séances...`); 
      (async () => {
        try {
          const response = await fetch(`http://localhost:10000/api/v1/sessions/by_sequence/${newlyExpandedItemId}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const sessions = await response.json();
          console.log(`Séances reçues pour séquence ${newlyExpandedItemId}:`, sessions);

          const formattedSessions = sessions.map(session => ({
            id: session.id,
            name: session.title || `Séance ${session.id}`,
            type: 'seance',
            children: [{ id: `loading-res-${session.id}`, name: 'Chargement ressources...', type: 'loading' }] // Dummy child for resources
          }));

          updateNodeChildrenImmutable(newlyExpandedItemId, formattedSessions);

        } catch (error) {
          console.error("Erreur lors du chargement des séances:", error);
          updateNodeChildrenImmutable(newlyExpandedItemId, [{ id: `error-ses-${newlyExpandedItemId}`, name: 'Erreur chargement séances', type: 'error' }]);
        }
      })();
    } 
    // --- LOAD RESOURCES --- 
    else if (nodeToExpand && nodeToExpand.type === 'seance' && nodeToExpand.children.length === 1 && nodeToExpand.children[0].type === 'loading') {
      console.log(`CONDITION REMPLIE pour SÉANCE ${newlyExpandedItemId}. Chargement des ressources...`); 
      (async () => {
        try {
          const response = await fetch(`http://localhost:10000/api/v1/resources/by_session/${newlyExpandedItemId}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const resources = await response.json();
          console.log(`Ressources reçues pour séance ${newlyExpandedItemId}:`, resources);

          const formattedResources = resources.map(res => ({
            id: res.id,
            name: res.title || `Ressource ${res.id}`,
            type: 'resource', // Internal type for the TreeView
            url: res.description, // API uses 'description' for URL?
            resource_type: res.type, // API uses 'type'
            children: [] // Resources are leaves
          }));

          updateNodeChildrenImmutable(newlyExpandedItemId, formattedResources);

        } catch (error) {
          console.error("Erreur lors du chargement des ressources:", error);
          updateNodeChildrenImmutable(newlyExpandedItemId, [{ id: `error-res-${newlyExpandedItemId}`, name: 'Erreur chargement ressources', type: 'error' }]);
        }
      })();
    }
  };

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          top: '64px', 
          height: 'calc(100% - 64px)',
        },
      }}
      variant="persistent"
      anchor="left"
      open={open}
    >
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          padding: '16px',
          borderBottom: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.paper',
        }}
      >
        <IconButton onClick={open ? handleDrawerClose : handleDrawerOpen}>
          {open ? <ChevronLeftIcon /> : <MenuIcon />}
        </IconButton>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          Navigation
        </Typography>
      </Box>

      <Box sx={{ p: 2 }}>
        <ResourceButton />
      </Box>

      <Divider sx={{ my: 2 }} />

      <Box sx={{ overflow: 'auto', height: 'calc(100vh - 120px)' }}>
        {isLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', pt: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Box sx={{ p: 2 }}>
            <Typography color="error">{error}</Typography>
          </Box>
        ) : (
          <SimpleTreeView
            aria-label="progressions tree"
            sx={{ flexGrow: 1, width: '100%', overflowY: 'auto', padding: 1 }} 
            expanded={expandedItems} 
            onExpandedItemsChange={handleExpandedItemsChange} 
          >
            {renderedTreeNodes} 
          </SimpleTreeView>
        )}
      </Box>
    </Drawer>
  );
}

export default SideTreeView;
