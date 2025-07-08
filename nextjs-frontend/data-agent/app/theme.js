// theme.js
import { createTheme } from '@mui/material/styles';

const appTheme = createTheme({
  palette: {
    mode: 'dark',
    background: {
      default: '#1e1e1e',
      paper: '#2a2a2a',
    },
    primary: {
      main: '#646cff',
    },
    secondary: {
      main: '#ff9800',
    },
    text: {
      primary: '#ffffff',
      secondary: '#cfcfcf',
    },
  },
  typography: {
    fontFamily: 'system-ui, Avenir, Helvetica, Arial, sans-serif',
  },
});

export default appTheme;
