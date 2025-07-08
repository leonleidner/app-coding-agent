'use client';

import React from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button,
  Typography, Grid, Box, IconButton, Divider, Chip
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import KeyboardIcon from '@mui/icons-material/Keyboard';
import GroupsIcon from '@mui/icons-material/Groups';
import CommitIcon from '@mui/icons-material/Commit';
import TerminalIcon from '@mui/icons-material/Terminal';
import PublishIcon from '@mui/icons-material/Publish';
import ModelTrainingIcon from '@mui/icons-material/ModelTraining';
import ExtensionIcon from '@mui/icons-material/Extension';
import StarIcon from '@mui/icons-material/Star';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import LightbulbIcon from '@mui/icons-material/Lightbulb';

const Highlight = ({ children }) => (
  <Typography component="span" color="primary.main" fontWeight="bold">{children}</Typography>
);

const CustomChip = ({ label }) => (
  <Chip label={label} color="primary" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
);

const HowItWorksDialog = ({ open, onClose }) => {
  return (
    <Dialog open={open} onClose={onClose} scroll="paper" maxWidth="md" fullWidth>
      <DialogTitle>
        How GenAI Coding Agent Works
        <IconButton aria-label="close" onClick={onClose} sx={{ position: 'absolute', right: 8, top: 8 }}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Grid container justifyContent="center" sx={{ mb: 2 }}>
          <Grid item xs={6} sm={4} md={2}>
            <img src="/images/question_mark.png" alt="How it works" style={{ maxWidth: '100px', margin: '0 auto' }} />
          </Grid>
        </Grid>
        <Typography paragraph>
          GenAI Coding Agent ist eine <Highlight>cutting-edge Lösung</Highlight>, die Generative AI nutzt...
        </Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><KeyboardIcon fontSize="small" /> User Input</Typography>
        <Typography paragraph>Benutzer geben einfache Prompts ein...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><GroupsIcon fontSize="small" /> AI Agent Activation</Typography>
        <Typography paragraph>Unser System setzt spezialisierte KI-Agenten ein...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><CommitIcon fontSize="small" /> Git Integration</Typography>
        <Typography paragraph>Der Agent interagiert mit Repositories...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><TerminalIcon fontSize="small" /> Coding Process</Typography>
        <Typography paragraph>Die KI-Agents modifizieren Code automatisch...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><PublishIcon fontSize="small" /> Code Push</Typography>
        <Typography paragraph>Commits erfolgen als "Coding Agent"...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><ModelTrainingIcon fontSize="small" /> Learning</Typography>
        <Typography paragraph>Der Agent lernt aus früherem Code...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><ExtensionIcon fontSize="small" /> Workflow Integration</Typography>
        <Typography paragraph>Kann manuell oder in CI/CD genutzt werden...</Typography>

        <Typography variant="h6" sx={{ mt: 3 }}><StarIcon fontSize="small" /> Benefits</Typography>
        <Box sx={{ mb: 2 }}>
          <CustomChip label="Automatisiert Coding-Aufgaben" />
          <CustomChip label="Einheitliche Coding-Standards" />
        </Box>

        <Typography variant="h6" sx={{ mt: 3 }}><RocketLaunchIcon fontSize="small" /> Getting Started</Typography>
        <Typography paragraph>Integrieren Sie ihn einfach ins Repo...</Typography>

        <Divider sx={{ my: 2 }} />
        <Typography paragraph textAlign="center" fontStyle="italic">
          <Highlight>GenAI Coding Agent: Empowering Development Through AI</Highlight> <LightbulbIcon fontSize="small" />
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Schließen</Button>
      </DialogActions>
    </Dialog>
  );
};

export default HowItWorksDialog;
