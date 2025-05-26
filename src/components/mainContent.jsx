// src/components/MainContent.jsx
import React, { useState, useEffect, useRef } from 'react';
import {
  Box, Typography, TextField, Button, Select, MenuItem, FormControl,
  InputLabel, Link, Stack, Paper, CircularProgress
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import { useTheme } from '@mui/material/styles';

// Importiere die ausgelagerte Dialog-Komponente
import HowItWorksDialog from './howItWorksDialog';

const MainContent = () => {
  const theme = useTheme();
  // Beibehaltene States aus deinem Code-Snippet
  const [repo, setRepo] = useState('leonleidner/CSS-JS-Image-Hover-Ef'); // Beispiel-Repo, falls noch genutzt
  const [branch, setBranch] = useState('main'); // Beispiel-Branch, falls noch genutzt
  const [taskInput, setTaskInput] = useState('');

  // States für LLM/CrewAI Interaktion und Logs
  const [llmResponse, setLlmResponse] = useState(''); // Für das Endergebnis von CrewAI
  const [crewLogs, setCrewLogs] = useState([]);     // Für die gestreamten Logs
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState('deepseek/deepseek-chat-v3-0324:free'); // Dein Standardmodell
  const [currentTaskId, setCurrentTaskId] = useState(null);

  // State für den "How it works"-Dialog
  const [howItWorksOpen, setHowItWorksOpen] = useState(false);

  const ws = useRef(null); // Ref für das WebSocket-Objekt
  const logsEndRef = useRef(null); // Ref zum automatischen Scrollen der Logs

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [crewLogs]); // Scrolle nach unten, wenn neue Logs hinzukommen

  // WebSocket schließen, wenn die Komponente unmounted wird oder eine neue Task ID kommt
  useEffect(() => {
    return () => {
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        console.log("WebSocket wird geschlossen (Cleanup).");
        ws.current.close();
      }
    };
  }, []); // Einmaliger Cleanup-Effekt beim Unmount

  const handleTaskInputChange = (event) => {
    setTaskInput(event.target.value);
  };

  const handleOpenHowItWorks = () => {
    setHowItWorksOpen(true);
  };

  const handleCloseHowItWorks = () => {
    setHowItWorksOpen(false);
  };

  const handleAskJules = async () => {
    if (!taskInput.trim()) {
      setError("Bitte gib eine Aufgabe ein.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setLlmResponse('');
    setCrewLogs([]);
    setCurrentTaskId(null);

    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      console.log("Schließe bestehende WebSocket-Verbindung.");
      ws.current.close();
    }

    try {
      const response = await fetch('http://localhost:8000/api/start_crew_task', { // Neuer Endpunkt
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task: taskInput, model_name: selectedModel }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.error_message || errorData.detail || `Fehler beim Starten des Tasks: ${response.status}`);
      }

      const data = await response.json();
      setCurrentTaskId(data.task_id);
      setCrewLogs(prev => [...prev, `[SYSTEM] CrewAI Task gestartet (ID: ${data.task_id.substring(0,8)}...). Warte auf Logs...`]);

      const socketUrl = `ws://localhost:8000/ws/logs/${data.task_id}`;
      ws.current = new WebSocket(socketUrl);

      ws.current.onopen = () => {
        console.log(`WebSocket verbunden für Task ID: ${data.task_id}`);
        setCrewLogs(prevLogs => [...prevLogs, `[SYSTEM] WebSocket verbunden.`]);
      };

      ws.current.onmessage = (event) => {
        const message = event.data;
        if (message.startsWith("[FINAL_RESULT]")) {
            try {
                const resultObj = JSON.parse(message.substring("[FINAL_RESULT]".length));
                setLlmResponse(resultObj.result);
                setCrewLogs(prevLogs => [...prevLogs, `[SYSTEM] CrewAI Prozess erfolgreich beendet.`]);
                setIsLoading(false);
                if (ws.current) ws.current.close(1000, "Task abgeschlossen");
            } catch (e) {
                console.error("Fehler beim Parsen des Endergebnisses:", e, message);
                setError("Fehler beim Verarbeiten des Endergebnisses.");
                setCrewLogs(prevLogs => [...prevLogs, `[SYSTEM-ERROR] Fehler beim Parsen des Endergebnisses.`]);
                setIsLoading(false);
            }
        } else if (message === "[END_OF_LOGS]") {
            setCrewLogs(prevLogs => [...prevLogs, `[SYSTEM] Alle Logs empfangen. Warte auf Endergebnis...`]);
            // Das isLoading bleibt true bis FINAL_RESULT kommt oder ein Fehler auftritt
        } else {
            setCrewLogs(prevLogs => [...prevLogs, message]);
        }
      };

      ws.current.onerror = (event) => {
        console.error("WebSocket Fehler:", event);
        setError("WebSocket Verbindungsfehler. Der Task könnte fehlgeschlagen sein.");
        setCrewLogs(prevLogs => [...prevLogs, `[SYSTEM-ERROR] WebSocket Verbindungsfehler.`]);
        setIsLoading(false);
      };

      ws.current.onclose = (event) => {
        console.log("WebSocket geschlossen:", event.reason, event.code, "Clean:", event.wasClean);
        if (!event.wasClean && isLoading) { // isLoading ist noch true, wenn es kein FINAL_RESULT gab
            setError("WebSocket-Verbindung wurde unerwartet geschlossen. Task-Status unklar.");
            setIsLoading(false);
        }
        // Wenn es clean geschlossen wurde (z.B. nach FINAL_RESULT), ist isLoading schon false.
      };

    } catch (err) {
      setError(err.message);
      setIsLoading(false);
      console.error("Fehler beim Senden der Aufgabe:", err);
    }
  };

  return (
    <>
      <Paper sx={{
        padding: 4,
        maxWidth: '1000px',
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
              <MenuItem value="google/gemini-flash-1.5:free">Google Gemini Flash 1.5</MenuItem>
              <MenuItem value="mistralai/mistral-7b-instruct:free">Mistral 7B Instruct</MenuItem>
              <MenuItem value="openai/gpt-4o-mini:free">OpenAI GPT-4o mini</MenuItem>
              {/* Füge hier weitere Modelle von OpenRouter hinzu, die ":free" sind oder für die du zahlst */}
            </Select>
          </FormControl>

        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask our Coding Agent to work on a task (e.g., 'Change the color of the theme to green.')"
          multiline
          rows={3}
          value={taskInput}
          onChange={handleTaskInputChange}
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
          onClick={handleAskJules}
          disabled={isLoading}
          sx={{ mb: 2, py: 1.5, borderRadius: '8px' }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : "Give me a plan"}
        </Button>

        {error && (
          <Typography color="error" sx={{ mt: 2, whiteSpace: 'pre-wrap' }}>
            Fehler: {error}
          </Typography>
        )}

        {(crewLogs.length > 0) && ( // Zeige Log-Box, wenn Logs vorhanden sind (oder isLoading und currentTaskId existiert)
          <Box sx={{ mt: 2, p: 2, border: `1px solid ${theme.palette.divider}`, borderRadius: '8px', maxHeight: '400px', overflowY: 'auto', backgroundColor: 'rgba(0,0,0,0.05)' }}>
            <Typography variant="subtitle2" sx={{ color: theme.palette.text.secondary }} gutterBottom>
              Agent Logs {currentTaskId ? `(Task: ${currentTaskId.substring(0,8)}...)` : ''}:
            </Typography>
            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all', fontSize: '12px', color: theme.palette.text.primary }}>
              {crewLogs.join('\n')}
            </pre>
            <div ref={logsEndRef} />
          </Box>
        )}

        {llmResponse && (
          <Box sx={{ mt: (crewLogs.length > 0 || error) ? 2 : 3, p: 2, backgroundColor: 'rgba(0,0,0,0.1)', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom>Ergebnis:</Typography>
            <Typography sx={{ whiteSpace: 'pre-wrap', maxHeight: '300px', overflowY: 'auto' }}>
              {llmResponse}
            </Typography>
          </Box>
        )}

        <Stack direction="row" spacing={2} justifyContent="center" sx={{ mt: 4 }}>
          <Button
            variant="outlined"
            startIcon={<PlayArrowIcon />}
            onClick={handleOpenHowItWorks}
            sx={{ color: 'text.secondary', borderColor: 'rgba(255,255,255,0.2)', borderRadius: '8px' }}
          >
            How it works
          </Button>
          <Button variant="outlined" startIcon={<LightbulbIcon />} sx={{ color: 'text.secondary', borderColor: 'rgba(255,255,255,0.2)', borderRadius: '8px' }}>
            Need inspiration?
          </Button>
        </Stack>
      </Paper>
      {/* How it Works Dialog Komponente */}
      <HowItWorksDialog open={howItWorksOpen} onClose={handleCloseHowItWorks} />
    </>
  );
};

export default MainContent;