# coding_agent_backend/main.py
import asyncio
import uuid
import sys  # Für stdout Umleitung
import io   # Für StringIO als Basis für unseren Stream
import traceback  # Für detaillierte Fehlerausgaben
import logging  # Für strukturiertes Logging
import os

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    BackgroundTasks,
    UploadFile,
    File,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

from dotenv import load_dotenv

# Lade Umgebungsvariablen (z.B. API Keys)
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Directory for uploaded CSV files
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
LATEST_UPLOADED_DATASET: Optional[str] = None

# Importiere Konfigurationen und Komponenten
from llm_config import manager_llm as global_manager_llm, google_api_key # get_dynamic_llm für Worker
from agents import managerAgent, WorkerAgents # Importiere auch den Manager-Agenten für Vergleiche
from tasks import data_science_tasks
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

# Mapping of running task IDs to asyncio tasks for cancellation
RUNNING_TASKS: Dict[str, asyncio.Task] = {}

# Pydantic-Modell für den Request-Body
class StartTaskRequest(BaseModel):
    task: str
    model_name: str
    user_dataset_description: Optional[str] = "Keine spezifische Dataset-Beschreibung angegeben."
    user_project_goal: Optional[str] = "Allgemeine Analyse durchführen."
    dataset_path: Optional[str] = None

# --- Asynchrone Crew Ausführung ---
async def run_crew_asynchronously(
    task_id: str,
    user_inputs: Dict[str, Any],
    selected_model_from_frontend: str, # Modell für Worker-Agenten
    connection_manager: ConnectionManager # ConnectionManager Instanz übergeben
):
    logger.info(f"Starte Crew für Task {task_id} mit Inputs: {user_inputs} und Worker-Modell: {selected_model_from_frontend}")
    custom_callback_handler = WebSocketCallbackHandler(websocket_manager=connection_manager, task_id=task_id)
    ##Agents
    lead_data_scientist = managerAgent().lead_data_scientist()
    data_gatherer = WorkerAgents().data_gatherer(LATEST_UPLOADED_DATASET)
    data_cleaner = WorkerAgents().data_cleaner()
    eda_agent = WorkerAgents().eda_agent()
    modeling_agent = WorkerAgents().modeling_agent()
    reporting_agent = WorkerAgents().reporting_agent()

    ##Tasks
    tasks = data_science_tasks()
    data_science_project_task = tasks.data_science_project_task(lead_data_scientist)
    data_gather_task = tasks.data_gather_task(data_gatherer, [data_science_project_task])
    data_clean_task = tasks.data_clean_task(data_cleaner, [data_gather_task])
    eda_task = tasks.eda_task(eda_agent, [data_clean_task])
    modeling_task = tasks.modeling_task(modeling_agent, [eda_task])
    reporting_task = tasks.reporting_task(reporting_agent, [data_science_project_task])


    data_science_crew = Crew(
        agents=[
            lead_data_scientist,
            reporting_agent
        ],
        tasks=[
            data_science_project_task,
            reporting_task
        ],
        process=Process.sequential,
        embedder=dict(
            provider="google",
            config=dict(
                model="gemini-embedding-exp-03-07",
                api_key=google_api_key
            )
        ),
        manager_llm=global_manager_llm,
        verbose=True,
        callbacks=[custom_callback_handler],
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
            json_compatible_result = json.dumps({"result": final_result})
        except TypeError:
            json_compatible_result = json.dumps({"result": str(final_result)}) # Fallback auf String-Repräsentation

        await connection_manager.send_log_to_task(task_id, f"[FINAL_RESULT]{json_compatible_result}")
        logger.info(f"Crew für Task {task_id} beendet. Ergebnis (gekürzt): {str(final_result)[:200]}")

    except asyncio.CancelledError:
        if sys.stdout == ws_stream:
            sys.stdout = original_stdout
        ws_stream.flush()
        await connection_manager.send_log_to_task(task_id, "[SYSTEM] Task cancelled by user.")
        await connection_manager.send_log_to_task(task_id, "[FINAL_RESULT]{\"error\": \"cancelled\"}")
        return
    
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

@app.post("/api/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    """Receive a CSV file upload and store it on the server."""
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    LATEST_UPLOADED_DATASET = file_location
    return {"file_path": file_location}

@app.get("/api/datasets")
async def list_datasets():
    """Return dataset names and full paths from the uploads directory."""
    datasets = [
        {"name": f, "path": os.path.join(UPLOAD_DIR, f)}
        for f in os.listdir(UPLOAD_DIR)
        if os.path.isfile(os.path.join(UPLOAD_DIR, f))
    ]
    return {"datasets": datasets}

@app.post("/api/start_crew_task")
async def start_crew_task_endpoint(request_data: StartTaskRequest): 
    task_id = str(uuid.uuid4())
    logger.info(f"Neue Aufgabe gestartet: Task ID {task_id}, User Task: '{request_data.task}', Modell: {request_data.model_name}")

    dataset_path = request_data.dataset_path or LATEST_UPLOADED_DATASET or ""
    crew_inputs = {
        "user_dataset_description": request_data.user_dataset_description,
        "user_project_goal": request_data.user_project_goal,
        "user_raw_query": request_data.task,
        # Die folgenden sind wichtig, wenn deine Agenten-Goals/Tasks diese Platzhalter verwenden
        "dataset_description": request_data.user_dataset_description,
        "dataset_path": dataset_path,
        "project_goal": request_data.user_project_goal,
        # Platzhalter für Agenten, die sequenziell Ergebnisse austauschen. Standardwerte
        # verhindern KeyError, wenn spätere Agenten ihre Eingaben interpolieren.
        #"input_data_summary": "Rohdaten werden vom Data Gatherer bereitgestellt.",
        #"cleaned_data_summary": "Bereinigte Daten werden vom Data Cleaner bereitgestellt.",
        #"eda_insights": "EDA Ergebnisse werden vom EDA Agent bereitgestellt.",
        #"model_details_and_performance": "Modellergebnisse werden vom Modeling Agent bereitgestellt.",
        #"gathered_data_summary": "Details zur Datensammlung werden vom Data Gatherer bereitgestellt."
    }

    task = asyncio.create_task(
        run_crew_asynchronously(
            task_id,
            crew_inputs,
            request_data.model_name,
            manager,
        )
    )
    RUNNING_TASKS[task_id] = task

    return {"message": "CrewAI Task gestartet", "task_id": task_id}

@app.post("/api/cancel_task/{task_id}")
async def cancel_task(task_id: str):
    """Request cancellation of a running task."""
    task = RUNNING_TASKS.get(task_id)
    if task and not task.done():
        task.cancel()
        return {"message": f"Cancellation requested for {task_id}"}
    return {"message": f"Task {task_id} not running"}

@app.websocket("/ws/logs/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(websocket, task_id)
    try:
        while True:
            data = await websocket.receive_text()
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