// src/theme.js
import { createTheme } from '@mui/material/styles';
import { grey } from '@mui/material/colors';

const theme = createTheme({
  palette: {
    mode: 'dark', // Aktiviert den Dark Mode
    primary: {
      main: "#E67117", // Du kannst die Primärfarbe anpassen
    },
    background: {
      default: '#1a1a1a',
      paper: '#212121',   // Für Oberflächen wie Karten, Menüs
    },
    text: {
      primary: '#e0e0e0',
      secondary: grey[500],
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        colorPrimary: {
          backgroundColor: '#27293d' // Beispiel für AppBar-Farbe
        }
      }
    },
    MuiButton: {
        styleOverrides: {
            root: {
                textTransform: 'none', // Buttons oft ohne Großschreibung im UI
            }
        }
    }
  }
});

export default theme;