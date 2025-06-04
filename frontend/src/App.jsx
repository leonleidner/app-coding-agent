// src/App.jsx
import React, { useState } from 'react';
import { ThemeProvider, CssBaseline, Box, useTheme } from '@mui/material';
import appTheme from './theme';
import Sidebar from './components/sidebar';
import MainContent from './components/mainContent';

export const EXPANDED_SIDEBAR_WIDTH = 280;
export const COLLAPSED_SIDEBAR_WIDTH = 70; // Oder welche Breite deine zugeklappte Sidebar hat

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const theme = useTheme();

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const currentSidebarWidth = isSidebarOpen ? EXPANDED_SIDEBAR_WIDTH : COLLAPSED_SIDEBAR_WIDTH;

  return (
    <ThemeProvider theme={appTheme}>
      <CssBaseline />
      <Box sx={{ height: '100vh', backgroundColor: appTheme.palette.background.default, position: 'relative' }}>
        <Sidebar
          isOpen={isSidebarOpen}
          toggleSidebar={toggleSidebar}
          width={currentSidebarWidth}
        />
        <Box
          component="main"
          sx={{
            // position: 'absolute', top:0, left:0, right:0, bottom:0 // Eine Möglichkeit
            width: '100vw', // Füllt die gesamte Viewport-Breite
            height: '100vh',// Füllt die gesamte Viewport-Höhe
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',    // Zentriert Paper horizontal im Viewport
            justifyContent: 'center',// Zentriert Paper vertikal im Viewport
            position: 'relative',   // Für den absolut positionierten Footer
            padding: theme.spacing(5), // z.B. 40px Abstand zu den Viewport-Rändern
            boxSizing: 'border-box', // Damit Padding in width/height eingerechnet wird
          }}
        >
          <MainContent />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;