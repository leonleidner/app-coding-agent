# coding_agent_backend/main.py
import asyncio
import uuid
import sys # Für stdout Umleitung
import io  # Für StringIO als Basis für unseren Stream
import traceback # Für detaillierte Fehlerausgaben
import logging # Für strukturiertes Logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

from dotenv import load_dotenv

# Lade Umgebungsvariablen (z.B. API Keys)
load_dotenv()

# Logging konfigurieren (ganz am Anfang, nach den Imports)
logging.basicConfig(
    level=logging.INFO, # Setze auf logging.DEBUG für noch mehr Details
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Importiere Konfigurationen und Komponenten
from llm_config import manager_llm as global_manager_llm # get_dynamic_llm für Worker
from agents import list_of_all_agents, lead_data_scientist # Importiere auch den Manager-Agenten für Vergleiche
from tasks import data_science_project_task
# Stelle sicher, dass WebSocketStream auch importiert wird, falls es in callback_handler.py ist
from callback_handler import WebSocketCallbackHandler, WebSocketStream
from crewai import Crew, Process

# Langchain Debugging (kann sehr gesprächig sein, ggf. für Produktion auf False setzen)
import langchain
langchain.debug = True # Oder os.getenv("LANGCHAIN_DEBUG", "False").lower() == "true"

app = FastAPI()

# CORS-Einstellungen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173", "http://localhost:3000"], # 5173 hinzugefügt, falls Vite es nutzt
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- WebSocket Connection Management ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.logger = logging.getLogger(f"{__name__}.ConnectionManager")

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = []
        self.active_connections[task_id].append(websocket)
        self.logger.info(f"WebSocket connected für Task {task_id}: {websocket.client}")

    def disconnect(self, websocket: WebSocket, task_id: str):
        if task_id in self.active_connections:
            try:
                self.active_connections[task_id].remove(websocket)
                if not self.active_connections[task_id]:
                    del self.active_connections[task_id]
            except ValueError:
                self.logger.warning(f"WebSocket war bereits von Task {task_id} entfernt: {websocket.client}")
        self.logger.info(f"WebSocket disconnected für Task {task_id}: {websocket.client}")

    async def send_log_to_task(self, task_id: str, message: str):
        if task_id in self.active_connections:
            connections_for_task = list(self.active_connections[task_id])
            for connection in connections_for_task:
                try:
                    await connection.send_text(message)
                except WebSocketDisconnect:
                    self.logger.info(f"Client für Task {task_id} (send_log_to_task) hat Verbindung getrennt: {connection.client}")
                    self.disconnect(connection, task_id)
                except Exception as e:
                    self.logger.error(f"Fehler beim Senden der Log-Nachricht an {connection.client} für Task {task_id}: {e}")

    async def close_connections_for_task(self, task_id: str, reason_code: int = 1000, reason_text: str = "Task completed"):
        if task_id in self.active_connections:
            connections_to_close = list(self.active_connections[task_id])
            for connection in connections_to_close:
                try:
                    await connection.close(code=reason_code) # reason argument ist in manchen Libs optional oder anders
                    self.logger.info(f"WebSocket für Task {task_id} aktiv geschlossen: {connection.client} mit Code {reason_code}")
                except Exception as e:
                    self.logger.error(f"Fehler beim aktiven Schließen der WebSocket-Verbindung für {connection.client} Task {task_id}: {e}")
                finally:
                    if connection in self.active_connections.get(task_id, []):
                        self.disconnect(connection, task_id)
            self.logger.info(f"Alle WebSocket-Verbindungen für Task {task_id} finalisiert.")


manager = ConnectionManager()

# Pydantic-Modell für den Request-Body
class StartTaskRequest(BaseModel):
    task: str
    model_name: str
    user_dataset_description: Optional[str] = "Keine spezifische Dataset-Beschreibung angegeben."
    user_project_goal: Optional[str] = "Allgemeine Analyse durchführen."

# --- Asynchrone Crew Ausführung ---
async def run_crew_asynchronously(
    task_id: str,
    user_inputs: Dict[str, Any],
    selected_model_from_frontend: str, # Modell für Worker-Agenten
    connection_manager: ConnectionManager # ConnectionManager Instanz übergeben
):
    logger.info(f"Starte Crew für Task {task_id} mit Inputs: {user_inputs} und Worker-Modell: {selected_model_from_frontend}")

    custom_callback_handler = WebSocketCallbackHandler(websocket_manager=connection_manager, task_id=task_id)

    current_run_agents = []
    for agent_template in list_of_all_agents:
        if agent_template.role == lead_data_scientist.role:
            current_run_agents.append(agent_template)
        else:
            # Erstelle hier eine NEUE Instanz oder tiefe Kopie des Agenten
            # und weise das worker_llm_instance zu.
            # Beispiel: Annahme, Agenten sind Klassen oder haben eine Methode zum Setzen des LLM
            # import copy # Am Anfang der Datei
            # worker_agent = copy.deepcopy(agent_template)
            # worker_agent.llm = worker_llm_instance
            # current_run_agents.append(worker_agent)
            
            # Sicherste Variante: Agenten-Erstellungsfunktionen verwenden (nicht hier gezeigt)
            # Für dieses Beispiel vereinfacht (kann bei globalen Objekten zu Problemen führen,
            # aber CrewAI erstellt oft interne Kopien):
            current_run_agents.append(agent_template)


    data_science_crew = Crew(
        agents=current_run_agents,
        tasks=[data_science_project_task],
        process=Process.hierarchical,
        manager_llm=global_manager_llm,
        verbose=True, # Ermöglicht CrewAI's print() Ausgaben
        callbacks=[custom_callback_handler]
    )

    original_stdout = sys.stdout
    # event_type_prefix für die rohen CrewAI Konsolenlogs, die über WebSocket gestreamt werden
    ws_stream = WebSocketStream(
        custom_callback_handler,
        original_stdout,
        event_type_prefix="CrewAI Console",
        loop=asyncio.get_running_loop(),
    )

    try:
        await connection_manager.send_log_to_task(task_id, f"[SYSTEM] CrewAI Prozess wird gestartet. (Manager: {global_manager_llm.model})...")
        
        sys.stdout = ws_stream # Leite stdout um, um CrewAI's print() Ausgaben abzufangen
        
        final_result = await asyncio.to_thread(data_science_crew.kickoff, inputs=user_inputs)
        
        sys.stdout = original_stdout # Stelle stdout sofort nach kickoff wieder her
        ws_stream.flush() # Sende verbleibende gepufferte Logs vom Stream

        # Sende das Endergebnis
        # Stelle sicher, dass final_result in ein JSON-kompatibles Format gebracht wird, falls es ein Objekt ist
        import json
        try:
            # Versuche, es direkt zu serialisieren. Wenn es ein komplexes Objekt ist,
            # musst du vielleicht nur bestimmte Teile davon nehmen.
            json_compatible_result = json.dumps({"result": final_result})
        except TypeError:
            json_compatible_result = json.dumps({"result": str(final_result)}) # Fallback auf String-Repräsentation

        await connection_manager.send_log_to_task(task_id, f"[FINAL_RESULT]{json_compatible_result}")
        logger.info(f"Crew für Task {task_id} beendet. Ergebnis (gekürzt): {str(final_result)[:200]}")

    except Exception as e:
        if sys.stdout == ws_stream: # Nur wiederherstellen, wenn es noch umgeleitet ist
            sys.stdout = original_stdout
        ws_stream.flush() # Sende verbleibende Logs auch im Fehlerfall

        error_message_full = f"Fehler während der Crew-Ausführung für Task {task_id}: {e}\n{traceback.format_exc()}"
        logger.error(error_message_full)
        await connection_manager.send_log_to_task(task_id, f"[SYSTEM-ERROR] {str(e)}")
        await connection_manager.send_log_to_task(task_id, f"[FINAL_RESULT]{{\"error\": \"{str(e)}\"}}")
    finally:
        if sys.stdout == ws_stream:
            sys.stdout = original_stdout # Endgültige Wiederherstellung
        await connection_manager.close_connections_for_task(task_id)

# --- API Endpunkte ---
@app.post("/api/start_crew_task")
async def start_crew_task_endpoint(request_data: StartTaskRequest, background_tasks: BackgroundTasks): # Umbenannt, um Konflikt mit importiertem Task zu vermeiden
    task_id = str(uuid.uuid4())
    logger.info(f"Neue Aufgabe gestartet: Task ID {task_id}, User Task: '{request_data.task}', Modell: {request_data.model_name}")

    crew_inputs = {
        "user_dataset_description": request_data.user_dataset_description,
        "user_project_goal": request_data.user_project_goal,
        "user_raw_query": request_data.task,
        # Die folgenden sind wichtig, wenn deine Agenten-Goals/Tasks diese Platzhalter verwenden
        "dataset_description": request_data.user_dataset_description,
        "project_goal": request_data.user_project_goal,
        # Platzhalter für Agenten, die sequenziell Ergebnisse austauschen. Standardwerte
        # verhindern KeyError, wenn spätere Agenten ihre Eingaben interpolieren.
        "input_data_summary": "Rohdaten werden vom Data Gatherer bereitgestellt.",
        "cleaned_data_summary": "Bereinigte Daten werden vom Data Cleaner bereitgestellt.",
        "eda_insights": "EDA Ergebnisse werden vom EDA Agent bereitgestellt.",
        "model_details_and_performance": "Modellergebnisse werden vom Modeling Agent bereitgestellt.",
        "gathered_data_summary": "Details zur Datensammlung werden vom Data Gatherer bereitgestellt."
    }

    background_tasks.add_task(
        run_crew_asynchronously,
        task_id,
        crew_inputs,
        request_data.model_name, # Modell für Worker
        manager # Die ConnectionManager-Instanz
    )

    return {"message": "CrewAI Task gestartet", "task_id": task_id}

@app.websocket("/ws/logs/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(websocket, task_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Optional: Auf Ping/Pong oder andere Client-Nachrichten reagieren
            # logger.debug(f"Nachricht vom Client für Task {task_id}: {data}")
    except WebSocketDisconnect:
        logger.info(f"Client für Task {task_id} (WebSocket Endpoint) hat Verbindung getrennt.")
    except Exception as e:
        logger.error(f"Unerwarteter Fehler im WebSocket für Task {task_id}: {e}")
    finally:
        # Disconnect wird aufgerufen, wenn die Schleife endet (durch Disconnect oder Fehler)
        manager.disconnect(websocket, task_id)


# --- Uvicorn Start (für die lokale Entwicklung) ---
if __name__ == "__main__":
    import uvicorn
    # Stelle sicher, dass der Host 0.0.0.0 ist, wenn du von einem anderen Gerät/Container zugreifen willst
    # oder 127.0.0.1, wenn nur lokal.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)