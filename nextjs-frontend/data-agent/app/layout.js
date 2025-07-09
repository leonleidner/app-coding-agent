'use client';

import React, { useState } from 'react';
import { CssBaseline, Box, useTheme, ThemeProvider } from '@mui/material';
import appTheme from '../app/theme';
import Sidebar from '../app/components/sidebar';
import '../app/styles/index.css';
import '../app/styles/App.css';
import { DatasetProvider } from '../app/context/DatasetContext';

export const EXPANDED_SIDEBAR_WIDTH = 225;
export const COLLAPSED_SIDEBAR_WIDTH = 70;

export default function RootLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [datasetPath, setDatasetPath] = useState('');
  const [refreshSidebarKey, setRefreshSidebarKey] = useState(0);

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
  const currentSidebarWidth = isSidebarOpen ? EXPANDED_SIDEBAR_WIDTH : COLLAPSED_SIDEBAR_WIDTH;

  const handleDatasetUpload = () => {
    setRefreshSidebarKey((prev) => prev + 1);
  };

  const childrenWithProps = React.cloneElement(children, {
    onDatasetUploaded: handleDatasetUpload
  });

  return (
    <html lang="en">
      <head>
        <title>Leon&apos;s - Data Science Agent App</title>
        <link rel="icon" type="image/png" href="/images/agent1.png" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body>
        <ThemeProvider theme={appTheme}>
          <DatasetProvider>
            <CssBaseline />
            <Box sx={{ height: '100vh', backgroundColor: appTheme.palette.background.default, position: 'relative' }}>
              <Sidebar
                key={refreshSidebarKey}
                isOpen={isSidebarOpen}
                toggleSidebar={toggleSidebar}
                width={currentSidebarWidth}
                onSelectDataset={(path) => setDatasetPath(path)}
              />
              <Box
                component="main"
                sx={{
                  width: '100vw',
                  height: '100vh',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: 5,
                  boxSizing: 'border-box',
                  overflowY: 'hidden',
                  overflowX: 'hidden',
                  ml: `${currentSidebarWidth}px`,
                }}
              >
                {childrenWithProps}
              </Box>
            </Box>
          </DatasetProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}