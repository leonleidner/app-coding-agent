'use client';

import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Box, Typography, TextField, IconButton, CircularProgress, Paper, Tooltip, Snackbar, Alert
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import CloseIcon from '@mui/icons-material/Close';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { useTheme } from '@mui/material/styles';
import { useDataset } from '../context/DatasetContext';
import AnsiToHtml from 'ansi-to-html';

const MainContent = () => {
  const theme = useTheme();
  const { datasetPath, setDatasetPath } = useDataset();

  const [taskInput, setTaskInput] = useState('');
  const [crewLogs, setCrewLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showSnackbar, setShowSnackbar] = useState(false);

  const ws = useRef(null);
  const logsEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const ansiConverter = useMemo(() => new AnsiToHtml({ newline: true }), []);

  const logsHtml = useMemo(() => ansiConverter.toHtml(
    crewLogs.map(line => {
      // -----------------------------------------------------------------
      // 1. Spezifische Manager-Regeln (müssen zuerst geprüft werden!)
      // -----------------------------------------------------------------
      if (line.includes('# Agent: Project Manager')) {
        return `<span style="color:#8E44AD; font-weight:bold;">🧑‍💼 ${line}</span>`;
      }
      if (line.includes('# Agent: Crew Manager')) {
        return `<span style="color:#2980B9; font-weight:bold;"> orchestrator ${line}</span>`;
      }
      if (line.includes('# Agent: Data Insights Communicator')) {
        return `<span style="color:#16A085; font-weight:bold;">📊 ${line}</span>`;
      }
  
      // -----------------------------------------------------------------
      // 2. Allgemeinen Regeln (kommen nach den spezifischen)
      // -----------------------------------------------------------------
      if (line.includes('# Agent:')) { // Fängt alle anderen Agenten ab
        return `<span style="color:#82b1ff;">${line}</span>`;
      }
      if (line.includes('[FINAL_RESULT]')) {
        return `<span style="color:#80cbc4; font-weight:bold;">${line}</span>`;
      }
      if (line.includes('[SYSTEM]')) {
        return `<span style="color:#ffb74d;">${line}</span>`;
      }
      if (line.includes('[SYSTEM-ERROR]')) {
        return `<span style="color:#ef5350; font-weight:bold;">${line}</span>`;
      }
      
      // 3. Fallback für alle anderen Zeilen
      return line;
  
    }).join('\n')
  ), [crewLogs, ansiConverter]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [crewLogs]);

  useEffect(() => () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) ws.current.close();
  }, []);

  const handleAskAgent = async () => {
    if (!taskInput.trim()) {
      setError("Bitte gib eine Aufgabe ein.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setCrewLogs([]);

    if (ws.current && ws.current.readyState === WebSocket.OPEN) ws.current.close();

    try {
      const response = await fetch('http://localhost:8000/api/start_crew_task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: taskInput, model_name: "deepseek/deepseek-chat-v3-0324:free", dataset_path: datasetPath }),
      });

      if (!response.ok) throw new Error("Task konnte nicht gestartet werden.");

      const data = await response.json();
      const socketUrl = `ws://localhost:8000/ws/logs/${data.task_id}`;
      ws.current = new WebSocket(socketUrl);

      ws.current.onmessage = (event) => setCrewLogs(prev => [...prev, event.data]);
      ws.current.onerror = () => { setError("WebSocket Fehler"); setIsLoading(false); };
      ws.current.onclose = () => setIsLoading(false);

    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8000/api/upload_csv', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setDatasetPath(data.file_path);
          setShowSnackbar(true);
        } else {
          throw new Error("Fehler beim Hochladen der Datei");
        }
      } catch (err) {
        setError(err.message);
      }
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        width: '100%',
        maxWidth: '1100px',
        height: 'calc(100vh - 80px)',
        justifyContent: 'space-between',
        gap: 2,
        p: 3,
        m: '0 auto',
      }}
    >
      <Box sx={{ flexGrow: 1 }}>
        {crewLogs.length === 0 && (
          <Box textAlign="center">
            <Typography variant="h5" color="text.secondary" gutterBottom>
              Willkommen bei deinem Data Science Agent 👋
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Lade ein Dataset hoch oder formuliere eine Aufgabe, um zu starten.
            </Typography>
          </Box>
        )}

        {crewLogs.length > 0 && (
          <Box
            sx={{
              backgroundColor: '#2a2a2a',
              borderRadius: 4,
              p: 2,
              maxHeight: '500px',
              overflowY: 'auto',
              fontFamily: 'monospace',
              fontSize: '0.85rem',
              lineHeight: 1.5,
              color: '#e0e0e0',
              boxShadow: '0px 2px 8px rgba(0,0,0,0.2)',
            }}
            dangerouslySetInnerHTML={{ __html: logsHtml }}
          />
        )}

        <div ref={logsEndRef} />

        {error && <Typography color="error">Fehler: {error}</Typography>}
      </Box>

      <Paper
        sx={{
          display: 'flex',
          alignItems: 'center',
          px: 2,
          py: 1,
          borderRadius: 4,
          backgroundColor: theme.palette.background.paper,
          boxShadow: '0 0 4px rgba(0,0,0,0.3)'
        }}
      >
        {datasetPath && (
          <Tooltip title={`Aktives Dataset: ${datasetPath.split('/').pop()}`} placement="top">
            <Box sx={{ display: 'flex', alignItems: 'center', mr: 1 }}>
              <InsertDriveFileIcon sx={{ color: theme.palette.primary.main }} />
              <IconButton size="small" onClick={() => setDatasetPath('')} sx={{ ml: -1 }}>
                <CloseIcon fontSize="small" />
              </IconButton>
            </Box>
          </Tooltip>
        )}

        <TextField
          fullWidth
          multiline
          maxRows={6}
          placeholder="Stelle eine Aufgabe an den Agenten..."
          value={taskInput}
          onChange={(e) => setTaskInput(e.target.value)}
          variant="standard"
          InputProps={{ disableUnderline: true }}
          sx={{ px: 1 }}
        />

        <IconButton component="label">
          <UploadFileIcon />
          <input
            type="file"
            accept=".csv"
            hidden
            ref={fileInputRef}
            onChange={handleFileChange}
          />
        </IconButton>

        <IconButton
          color="primary"
          onClick={handleAskAgent}
          disabled={isLoading}
        >
          {isLoading ? <CircularProgress size={20} /> : <SendIcon />}
        </IconButton>
      </Paper>

      <Snackbar
        open={showSnackbar}
        autoHideDuration={3000}
        onClose={() => setShowSnackbar(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setShowSnackbar(false)} severity="success" sx={{ width: '100%' }}>
          CSV-Datei erfolgreich hochgeladen und gesetzt!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MainContent;
