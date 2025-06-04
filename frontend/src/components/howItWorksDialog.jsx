// src/components/HowItWorksDialog.jsx
import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  IconButton,
  Typography,
  Grid,
  Divider,
  Chip,
  Box // Box hinzugefügt
} from '@mui/material';
import { useTheme } from '@mui/material/styles';

// MUI Icons (alle hier importieren, die im Dialog-Inhalt benötigt werden)
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
import CloseIcon from '@mui/icons-material/Close'; // Für den Schließen-Button im Titel

// Interne Komponente für den Inhalt des Dialogs
const HowItWorksDialogContent = () => {
  const theme = useTheme(); // theme hier holen, falls benötigt

  const Highlight = ({ children }) => (
    <Typography component="span" color="primary.main" sx={{ fontWeight: 'bold' }}>
      {children}
    </Typography>
  );

  const CustomChip = ({ label }) => (
    <Chip label={label} color="primary" size="small" sx={{ mr: 0.5, mb: 0.5, backgroundColor: theme.palette.primary.main, color: theme.palette.primary.contrastText }} />
  );

  return (
    <>
      <Grid container justifyContent="center" sx={{ mb: 2 }}>
        <Grid item xs={6} sm={4} md={2}>
          <img src="/images/question_mark.png" alt="How it works" style={{ width: '100%', maxWidth: '100px', display: 'block', margin: '0 auto' }} />
        </Grid>
      </Grid>
      <Typography variant="body1" paragraph>
        GenAI Coding Agent ist eine cutting-edge Lösung, die Generative AI nutzt, um den Softwareentwicklungsprozess zu revolutionieren. Durch den Einsatz mehrerer KI-Agenten <Highlight>automatisiert</Highlight> unser System <Highlight>Coding-Aufgaben</Highlight>, <Highlight>steigert die Produktivität</Highlight> und <Highlight>demokratisiert die Entwicklung</Highlight>. Hier ist eine Aufschlüsselung, wie es funktioniert:
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <KeyboardIcon sx={{ mr: 1 }} /> User Input
      </Typography>
      <Typography variant="body1" paragraph>
        Der Prozess beginnt mit der Benutzereingabe. Benutzer geben einen einfachen Prompt oder eine bestehende User Story ein, und das System akzeptiert eine breite Palette von Eingaben. Diese können von allgemeinen Feature-Anfragen bis hin zu spezifischen Code-Modifikationen variieren, was Flexibilität bei der Zuweisung von Aufgaben an den GenAI Coding Agent ermöglicht.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <GroupsIcon sx={{ mr: 1 }} /> AI Agent Activation
      </Typography>
      <Typography variant="body1" paragraph>
        Unser System setzt eine Crew von spezialisierten KI-Agenten ein, von denen jeder eine eigene Rolle hat:
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1, mb:3, textAlign: 'center' }}>
        <Grid item xs={12} sm={4}>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
            <img src="/images/agent1.png" alt="Product Manager Agent" style={{ width: '100%', maxWidth: '80px' }} />
          </Box>
          <Typography variant="h6" component="h3">Product Manager Agent</Typography>
          <Typography variant="caption" component="div" sx={{ px:1 }}>
            - Analysiert die Eingabe des Benutzers<br />
            - Erstellt einen umfassenden Implementierungsplan<br />
            - Priorisiert Aufgaben und bereitet die Entwicklung vor
          </Typography>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
            <img src="/images/agent2.png" alt="Software Engineer Agent" style={{ width: '100%', maxWidth: '80px' }} />
          </Box>
          <Typography variant="h6" component="h3">Software Engineer Agent</Typography>
          <Typography variant="caption" component="div" sx={{ px:1 }}>
            - Zerlegt den Implementierungsplan in umsetzbare Schritte<br />
            - Entwirft die Gesamtarchitektur und den Ansatz<br />
            - Stellt sicher, dass Best Practices und Coding-Standards eingehalten werden
          </Typography>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
            <img src="/images/agent3.png" alt="Developer Agent(s)" style={{ width: '100%', maxWidth: '80px' }} />
          </Box>
          <Typography variant="h6" component="h3">Developer Agent(s)</Typography>
          <Typography variant="caption" component="div" sx={{ px:1 }}>
            - Führt die eigentlichen Code-Änderungen aus<br />
            - Kann gleichzeitig an mehreren Dateien und Komponenten arbeiten<br />
            - Implementiert die erforderliche Funktionalität basierend auf dem Design des Software Engineers
          </Typography>
        </Grid>
      </Grid>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <CommitIcon sx={{ mr: 1 }} /> Git Integration
      </Typography>
      <Typography variant="body1" paragraph>
        GenAI Coding Agent verbindet sich nahtlos mit Ihren bestehenden Code-Repositories wie GitHub oder GitLab. Es zieht die notwendige Codebasis für Modifikationen und stellt sicher, dass alle Änderungen im Kontext Ihres aktuellen Projekts vorgenommen werden. Das System verfolgt diese Änderungen und ermöglicht eine umfassende Überprüfung, bevor Commits gemacht werden.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <TerminalIcon sx={{ mr: 1 }} /> Automated Coding Process
      </Typography>
      <Typography variant="body1" paragraph>
        Der automatisierte Codierungsprozess beginnt mit einer gründlichen Analyse der bestehenden Codebasis. KI-Agenten arbeiten zusammen, um die erforderlichen Änderungen vorzunehmen, indem sie Code nach Bedarf generieren, modifizieren oder refaktorisieren. Während dieses Prozesses werden Änderungen auf Kompatibilität und Funktionalität getestet, um sicherzustellen, dass sich der neue Code reibungslos in das bestehende System integriert.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <PublishIcon sx={{ mr: 1 }} /> Code Push and Review
      </Typography>
      <Typography variant="body1" paragraph>
        Sobald die Änderungen abgeschlossen sind, wird der modifizierte Code zurück in das Repository gepusht. Diese Änderungen erscheinen als Commits von "Coding Agent" in Ihrer Entwicklungsumgebung und ermöglichen eine nahtlose Integration in Ihren bestehenden Workflow. Ihr Team kann dann den von der KI generierten Code überprüfen, genehmigen oder Änderungen anfordern und behält so die volle Kontrolle über den Entwicklungsprozess.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <ModelTrainingIcon sx={{ mr: 1 }} /> Continuous Learning and Improvement
      </Typography>
      <Typography variant="body1" paragraph>
        Eine der Hauptfunktionen des GenAI Coding Agent ist seine Fähigkeit zu lernen und sich zu verbessern. Das System lernt aus jeder Interaktion und Code-Änderung und verbessert kontinuierlich sein Verständnis Ihrer Codebasis und Ihres Codierungsstils. Dies stellt sicher, dass die KI im Laufe der Zeit effizienter wird und sich besser an die Praktiken Ihres Teams anpasst.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <ExtensionIcon sx={{ mr: 1 }} /> Integration with Development Workflow
      </Typography>
      <Typography variant="body1" paragraph>
        GenAI Coding Agent ist so konzipiert, dass er sich nahtlos in Ihre bestehenden Entwicklungsprozesse einfügt. Er kann manuell für bestimmte Aufgaben ausgelöst oder für stärker automatisierte Workflows in CI/CD-Pipelines integriert werden, was Flexibilität bei der Nutzung seiner Fähigkeiten bietet.
      </Typography>

      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <StarIcon sx={{ mr: 1 }} /> Benefits
      </Typography>
      <Box sx={{mb: 2}}>
        <CustomChip label="Automatisiert repetitive Coding-Aufgaben." />
        <CustomChip label="Stellt sicher, dass Coding-Standards konsistent angewendet werden." />
        <CustomChip label="Ermöglicht nicht-technischen Teammitgliedern, zur Entwicklung beizutragen." />
        <CustomChip label="Verarbeitet mehrere Projekte und Codebasen." />
        <CustomChip label="Lernt und passt sich dem Codierungsstil und den Praktiken Ihres Teams an." />
      </Box>


      <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center', mt: 3 }}>
        <RocketLaunchIcon sx={{ mr: 1 }} /> Getting Started
      </Typography>
      <Typography variant="body1" paragraph>
        Um mit GenAI Coding Agent zu beginnen, integrieren Sie ihn einfach in Ihr Repository und starten Sie mit Ihrem ersten Prompt. Unser Team steht Ihnen während des gesamten Einrichtungsprozesses und darüber hinaus zur Seite.
      </Typography>
      <Typography variant="body1" paragraph>
        Für weitere Informationen oder um eine Demo anzufordern, kontaktieren Sie bitte unser Vertriebsteam.
      </Typography>
      <Divider sx={{ my: 2 }} />
      <Typography variant="body1" paragraph sx={{ fontStyle: 'italic', textAlign: 'center', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Highlight>GenAI Coding Agent: Empowering Development Through AI</Highlight> <LightbulbIcon sx={{ ml: 1, color: 'primary.main' }} />
      </Typography>
    </>
  );
};

// Die Haupt-Dialogkomponente, die exportiert wird
const HowItWorksDialog = ({ open, onClose }) => {
  const theme = useTheme(); // Theme für den Close-Button im Titel

  return (
    <Dialog
      open={open}
      onClose={onClose}
      scroll="paper"
      aria-labelledby="how-it-works-dialog-title"
      maxWidth="md"
      fullWidth
    >
      <DialogTitle id="how-it-works-dialog-title">
        How GenAI Coding Agent Works
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: theme.spacing(1),
            top: theme.spacing(1),
            color: theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <HowItWorksDialogContent />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Schließen
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default HowItWorksDialog;