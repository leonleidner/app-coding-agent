import React, { useState } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  IconButton,
  Tooltip,
  ListItemIcon
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DescriptionIcon from '@mui/icons-material/Description';
import ForumIcon from '@mui/icons-material/Forum';
import TwitterIcon from '@mui/icons-material/Twitter';
import FolderIcon from '@mui/icons-material/Folder';
import HistoryIcon from '@mui/icons-material/History';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { useTheme } from '@mui/material/styles';

const Sidebar = ({ isOpen, toggleSidebar, width }) => {
  const theme = useTheme();
  const [isCodebasesExpanded, setIsCodebasesExpanded] = useState(false); // Standardmäßig geöffnet

  const handleHistoryClick = () => {
    console.log("History button clicked");
    // Hier deine Logik für den History-Button
  };

  const handleCodebasesToggle = () => {
    if (isOpen) {
      setIsCodebasesExpanded(!isCodebasesExpanded);
    }
  };
  
  const commonListItemStyle = {
    pl: isOpen ? 4 : 'auto',
    justifyContent: isOpen ? 'initial' : 'center',
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
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
        borderRight: `1px solid ${theme.palette.divider}`,
        color: 'text.primary',
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: isOpen ? theme.transitions.duration.enteringScreen : theme.transitions.duration.leavingScreen,
        }),
      }}
    >
      <Box sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: isOpen ? 'space-between' : 'center',
        padding: theme.spacing(1.5, 2),
        minHeight: '64px',
        flexShrink: 0,
      }}>
        {isOpen && (
          <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', whiteSpace: 'nowrap' }}>
            Coding Agent <span style={{ color: theme.palette.text.secondary, fontSize: '0.8em' }}>beta</span>
          </Typography>
        )}
        <IconButton onClick={toggleSidebar} color="inherit" aria-label={isOpen ? "Sidebar schließen" : "Sidebar öffnen"} sx={{
            '&:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.08)', // Leichter Hover-Effekt für Dark Theme
            },
            // HIER WIRD DIE FOKUS-UMRANDUNG ANGEPASST
            '&.Mui-focusVisible': { 
              outline: `2px solid #E67117`, // Deine gewünschte Farbe und Stil
              outlineOffset: '2px',         // Optional: kleiner Abstand zwischen Icon und Umrandung
            }
          }}>
          {isOpen ? <ChevronLeftIcon /> : <MenuIcon />}
        </IconButton>
      </Box>
      <Divider sx={{ flexShrink: 0 }} />

      <Box sx={{ overflowY: 'auto', overflowX: 'hidden', flexGrow: 1 }}>
        {/* History Button */}
        <ListItem
          button
          onClick={handleHistoryClick}
          sx={{
            display: 'flex',
            flexDirection: isOpen ? 'row' : 'column',
            alignItems: 'center',
            justifyContent: isOpen ? 'flex-start' : 'center',
            padding: theme.spacing(0.5, isOpen ? 2 : 0.5),
            minHeight: isOpen ? '48px' : '56px',
            ...(!isOpen && {
                paddingTop: theme.spacing(1),
                paddingBottom: theme.spacing(1),
              }),
            '&:hover': {
              backgroundColor: theme.palette.action.hover,
            },
          }}
        >
          <Tooltip title={!isOpen ? "History" : ""} placement="right">
            <ListItemIcon sx={{
              minWidth: 0,
              justifyContent: 'center',
              mr: isOpen ? 2 : 0, // Margin rechts nur wenn Text da ist
              p: !isOpen ? theme.spacing(0.5) : 0,
            }}>
              <HistoryIcon
                fontSize="small"
                sx={{ color: theme.palette.text.primary }}
              />
            </ListItemIcon>
          </Tooltip>
          {isOpen && (
            <ListItemText
              primary="History"
              primaryTypographyProps={{
                variant: 'subtitle2',
                fontWeight: 'medium',
                whiteSpace: 'nowrap',
              }}
            />
          )}
        </ListItem>

        {/* Codebases Accordion */}
        <Accordion
          expanded={isOpen && isCodebasesExpanded}
          disabled={!isOpen}
          onChange={handleCodebasesToggle}
          sx={{
            backgroundImage: 'none',
            boxShadow: 'none',
            '&:before': { display: 'none' },
            '&.Mui-disabled': {
              backgroundColor: 'transparent',
            },
            margin: `0 !important`, // Wichtig um margin von Accordion zu resetten
            '& .MuiAccordionSummary-root.Mui-disabled': { // Styles für Summary wenn Accordion disabled
                 backgroundColor: 'transparent !important',
                 opacity: 1,
            },
          }}
        >
          <AccordionSummary
            expandIcon={isOpen ? <ExpandMoreIcon /> : null}
            aria-controls="codebases-content"
            id="codebases-header"
            sx={{
              flexDirection: isOpen ? 'row-reverse' : 'column',
              padding: theme.spacing(0.5, isOpen ? 2 : 0.5),
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: isOpen ? '48px' : '56px',
              cursor: !isOpen ? 'default' : 'pointer',
              '&.Mui-disabled': { // Redundant, da oben schon auf Accordion-Ebene, aber schadet nicht
                backgroundColor: 'transparent !important',
                opacity: 1,
              },
              '&:not(.Mui-disabled):hover': {
                 backgroundColor: isOpen ? theme.palette.action.hover : 'transparent',
              },
              '& .MuiAccordionSummary-content': {
                margin: 0,
                marginRight: isOpen ? theme.spacing(1) : 0,
                flexGrow: isOpen ? 1 : 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: isOpen ? 'flex-start' : 'center',
              },
              ...(!isOpen && {
                paddingTop: theme.spacing(1),
                paddingBottom: theme.spacing(1),
              })
            }}
          >
            <Tooltip title={isOpen ? "" : "Codebases"} placement="right">
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: !isOpen ? theme.spacing(0.5) : 0 }}>
                <FolderIcon
                  fontSize="small"
                  sx={{ color: !isOpen && !isCodebasesExpanded ? theme.palette.text.primary : theme.palette.action.active }}
                />
              </Box>
            </Tooltip>
            {isOpen && (
              <Typography variant="subtitle2" sx={{ fontWeight: 'medium', whiteSpace: 'nowrap', ml: isOpen ? 1: 0 }}>
                Codebases
              </Typography>
            )}
          </AccordionSummary>
          {isOpen && ( // Details nur rendern wenn Sidebar offen ist, expanded wird vom Accordion gehandhabt
            <AccordionDetails sx={{ padding: 0 }}>
              <List dense>
                {['leonleidner/CSS-JS-Image...', 'leonleidner/Fincrawl', 'leonleidner/StockSeason'].map((text) => (
                  <ListItem
                    button
                    key={text}
                    secondaryAction={
                      isOpen ? (
                        <IconButton edge="end" aria-label="add" size="small">
                          <AddIcon fontSize="small" />
                        </IconButton>
                      ) : null
                    }
                    sx={{ ...commonListItemStyle }}
                  >
                    {isOpen && <ListItemText primary={text} sx={{ opacity: isOpen ? 1 : 0, whiteSpace: 'nowrap' }} />}
                  </ListItem>
                ))}
              </List>
            </AccordionDetails>
          )}
        </Accordion>
      </Box>

      <Divider sx={{ flexShrink: 0 }} />

      <Box sx={{
        display: 'flex',
        justifyContent: isOpen ? 'space-around' : 'center',
        flexDirection: isOpen ? 'row' : 'column',
        alignItems: 'center',
        padding: theme.spacing(1),
        flexShrink: 0,
      }}>
        <Tooltip title={isOpen ? "" : "Docs"} placement="right">
          <IconButton size="small" color="inherit" aria-label="Docs">
            <DescriptionIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title={isOpen ? "" : "X (Twitter)"} placement="right">
          <IconButton size="small" color="inherit" aria-label="X (Twitter)">
            <TwitterIcon />
          </IconButton>
        </Tooltip>
      </Box>
    </Box>
  );
};

export default Sidebar;