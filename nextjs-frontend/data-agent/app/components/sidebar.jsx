'use client';

import React, { useState, useEffect } from 'react';
import {
  Box, Typography, List, ListItem, ListItemText, Accordion, AccordionSummary,
  AccordionDetails, Divider, IconButton, Tooltip, ListItemIcon
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FolderIcon from '@mui/icons-material/Folder';
import HistoryIcon from '@mui/icons-material/History';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import DescriptionIcon from '@mui/icons-material/Description';
import TwitterIcon from '@mui/icons-material/Twitter';
import { useTheme } from '@mui/material/styles';
import { useDataset } from '../context/DatasetContext';
import HowItWorksDialog from './howItWorksDialog';

const Sidebar = ({ isOpen, toggleSidebar, width }) => {
  const theme = useTheme();
  const { setDatasetPath } = useDataset();
  const [isDatasetsExpanded, setIsDatasetsExpanded] = useState(false);
  const [datasets, setDatasets] = useState([]);
  const [showHowItWorks, setShowHowItWorks] = useState(false);

  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        const resp = await fetch('http://localhost:8000/api/datasets');
        if (resp.ok) {
          const data = await resp.json();
          setDatasets(data.datasets || []);
        }
      } catch (err) {
        console.error('Fehler beim Laden der Datasets', err);
      }
    };
    fetchDatasets();
  }, []);

  const handleDatasetsToggle = () => {
    if (isOpen) setIsDatasetsExpanded(!isDatasetsExpanded);
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        left: 0,
        top: 0,
        height: '100vh',
        zIndex: theme.zIndex.drawer,
        width: width,
        bgcolor: 'background.paper',
        borderRight: `1px solid ${theme.palette.divider}`,
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: isOpen ? theme.transitions.duration.enteringScreen : theme.transitions.duration.leavingScreen,
        }),
        display: 'flex',
        flexDirection: 'column',
        overflowX: 'hidden',
      }}
    >
      {/* Header */}
      <Box sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: isOpen ? 'space-between' : 'center',
        padding: theme.spacing(1.5, 2),
        minHeight: '64px',
      }}>
        {isOpen && (
          <Typography variant="h6" fontWeight="bold">
            Data Agent <span style={{ fontSize: '0.8em', color: theme.palette.text.secondary }}>beta</span>
          </Typography>
        )}
        <IconButton onClick={toggleSidebar} aria-label="Toggle Sidebar">
          {isOpen ? <ChevronLeftIcon /> : <MenuIcon />}
        </IconButton>
      </Box>

      <Divider />

      {/* Datasets Accordion */}
      <Accordion
        expanded={isOpen && isDatasetsExpanded}
        disabled={!isOpen}
        onChange={handleDatasetsToggle}
        sx={{
          backgroundImage: 'none',
          boxShadow: 'none',
          '&:before': { display: 'none' },
          margin: `0 !important`,
        }}
      >
        <AccordionSummary
          expandIcon={isOpen ? <ExpandMoreIcon /> : null}
          aria-controls="datasets-content"
          id="datasets-header"
          sx={{
            flexDirection: isOpen ? 'row-reverse' : 'column',
            padding: theme.spacing(0.5, isOpen ? 2 : 0.5),
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: isOpen ? '48px' : '56px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: theme.palette.action.hover,
            },
            '& .MuiAccordionSummary-content': {
              margin: 0,
              flexGrow: isOpen ? 1 : 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: isOpen ? 'flex-start' : 'center',
            },
          }}
        >
          <Tooltip title={!isOpen ? "Datasets" : ""} placement="right">
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <FolderIcon fontSize="small" sx={{ color: theme.palette.text.primary }} />
            </Box>
          </Tooltip>
          {isOpen && (
            <Typography variant="subtitle2" sx={{ fontWeight: 'medium', ml: 1 }}>
              Datasets
            </Typography>
          )}
        </AccordionSummary>

        {isOpen && (
          <AccordionDetails sx={{ padding: 0 }}>
            <List dense>
              {datasets.map((ds) => (
                <ListItem
                  key={ds.path}
                  secondaryAction={
                    <IconButton edge="end" size="small" onClick={() => setDatasetPath(ds.path)}>
                      <AddIcon fontSize="small" />
                    </IconButton>
                  }
                  disablePadding
                >
                  <ListItemText primary={ds.name} sx={{ pl: 2 }} />
                </ListItem>
              ))}
            </List>
          </AccordionDetails>
        )}
      </Accordion>

      <Divider />

      {/* Footer Icons */}
      <Box sx={{ mt: 'auto', p: 1, display: 'flex', justifyContent: isOpen ? 'space-around' : 'center' }}>
        <Tooltip title="Docs">
            <IconButton onClick={() => setShowHowItWorks(true)}>
                <DescriptionIcon />
            </IconButton>
        </Tooltip>
        <Tooltip title="Twitter">
          <IconButton onClick={() => window.open('https://x.com', '_blank')}><TwitterIcon /></IconButton>
        </Tooltip>
      </Box>
      <HowItWorksDialog
        open={showHowItWorks}
        onClose={() => setShowHowItWorks(false)}
      />
    </Box>
  );
};

export default Sidebar;
