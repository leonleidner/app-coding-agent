// src/components/MainContent.jsx
import React, { useState } from 'react';
import {
  Box, Typography, TextField, Button, Select, MenuItem, FormControl,
  InputLabel, Link, Stack, Paper, CircularProgress // CircularProgress für Ladeanzeige
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import { useTheme } from '@mui/material/styles';

const MainContent = () => {
  const theme = useTheme();
  const [repo, setRepo] = useState('leonleidner/CSS-JS-Image-Hover-Ef'); // Beispiel-Repo
  const [branch, setBranch] = useState('main'); // Beispiel-Branch
  const [taskInput, setTaskInput] = useState(''); // Zustand für das Texteingabefeld
  
  // Neue Zustände für LLM-Interaktion
  const [llmResponse, setLlmResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState('deepseek/deepseek-chat-v3-0324:free'); // Standardmodell wie im Backend

  const handleTaskInputChange = (event) => {
    setTaskInput(event.target.value);
  };

  const handleAskCodingAgent = async () => {
    if (!taskInput.trim()) {
      setError("Bitte gib eine Aufgabe ein.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setLlmResponse('');

    try {
      const response = await fetch('http://localhost:8000/api/process_task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task: taskInput, model_name: selectedModel }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Fehler: ${response.status}`);
      }

      const data = await response.json();
      setLlmResponse(data.result);

    } catch (err) {
      setError(err.message);
      console.error("Fehler beim Senden der Aufgabe:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Paper sx={{
        padding: 4,
        maxWidth: '700px',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold', textAlign: 'center' }}>
          Meet PwC Coding Agent: an <span style={{ color: theme.palette.primary.main }}>async</span> development agent.
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" textAlign="center" gutterBottom>
          PwC Coding Agent tackles bugs, small feature requests, and other software engineering tasks, with direct export to GitHub.
        </Typography>

        {/* Modell Auswahl (optional, aber gut für Flexibilität) */}
        <FormControl fullWidth variant="outlined" size="small" sx={{ mt: 2, mb:1, backgroundColor: 'rgba(0,0,0,0.2)' }}>
            <InputLabel id="model-select-label" sx={{color: 'text.secondary'}}>Modell wählen</InputLabel>
            <Select
              labelId="model-select-label"
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              label="Modell wählen"
              IconComponent={ArrowDropDownIcon}
              sx={{ borderRadius: '8px', '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.2)' } }}
            >
              <MenuItem value="deepseek/deepseek-chat-v3-0324:free">Deepseek-v3-0324</MenuItem>
              <MenuItem value="google/gemini-2.0-flash-exp:free">Gemini-2.0-flash</MenuItem>
              {/* Füge hier weitere Modelle von OpenRouter hinzu */}
            </Select>
          </FormControl>

        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask our Coding Agent to work on a task (e.g., 'Change the color of the theme to green.')"
          multiline
          rows={3}
          value={taskInput} // Binde den Wert an den Zustand
          onChange={handleTaskInputChange} // Handle Änderungen
          sx={{
            mb: 2,
            backgroundColor: 'rgba(0,0,0,0.2)',
            borderRadius: '8px',
            '& .MuiOutlinedInput-root': {
              '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
              '&:hover fieldset': { borderColor: theme.palette.primary.main },
            },
          }}
        />

        <Button
          variant="contained"
          color="primary"
          size="large"
          fullWidth
          onClick={handleAskCodingAgent} // Klick-Handler
          disabled={isLoading} // Deaktiviere Button während des Ladens
          sx={{ mb: 2, py: 1.5, borderRadius: '8px' }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : "Give me a plan"}
        </Button>

        {/* Bereich für Fehlermeldungen und LLM-Antwort */}
        {error && (
          <Typography color="error" sx={{ mt: 2, whiteSpace: 'pre-wrap' }}>
            Fehler: {error}
          </Typography>
        )}
        {llmResponse && (
          <Box sx={{ mt: 3, p: 2, backgroundColor: 'rgba(0,0,0,0.1)', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom>Antwort:</Typography>
            <Typography sx={{ whiteSpace: 'pre-wrap', maxHeight: '300px', overflowY: 'auto' }}>
              {llmResponse}
            </Typography>
          </Box>
        )}

        <Stack direction="row" spacing={2} justifyContent="center" sx={{ mt: 4 }}>
          <Button variant="outlined" startIcon={<PlayArrowIcon />} sx={{ color: 'text.secondary', borderColor: 'rgba(255,255,255,0.2)', borderRadius: '8px' }}>
            How it works
          </Button>
          <Button variant="outlined" startIcon={<LightbulbIcon />} sx={{ color: 'text.secondary', borderColor: 'rgba(255,255,255,0.2)', borderRadius: '8px' }}>
            Need inspiration?
          </Button>
        </Stack>
      </Paper>
    </>
  );
};

export default MainContent;