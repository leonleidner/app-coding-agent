from langchain_core.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Union, Optional # Optional hinzugefügt für Klarheit
from uuid import UUID
import logging
import sys # Importiere sys für stdout Umleitung
import io  # Importiere io für StringIO
import asyncio # Für asyncio.create_task

logger = logging.getLogger(__name__)

class WebSocketCallbackHandler(BaseCallbackHandler):
    """
    Callback Handler, der Ausführungsinformationen an eine WebSocket-Verbindung streamt,
    verwaltet durch einen ConnectionManager.
    """

    def __init__(self, websocket_manager: Any, task_id: str):
        """
        Initialisiert den Callback Handler.

        Args:
            websocket_manager: Eine Instanz des ConnectionManager (aus main.py),
                               der eine Methode `send_log_to_task(task_id, message)` besitzt.
            task_id: Die eindeutige ID des aktuellen Tasks/Laufs.
        """
        super().__init__()
        self.websocket_manager = websocket_manager
        self.task_id = task_id
        self._log_prefix_str = f"[Task:{self.task_id[:8]}]" # Korrekte f-String Nutzung
        logger.info(f"{self._log_prefix_str} WebSocketCallbackHandler initialisiert.") # Korrekte f-String Nutzung

    async def _send_log(self, event_type: str, content: str, is_raw_crewai_output: bool = False): # Parameter hinzugefügt
        """
        Formatiert und sendet eine Log-Nachricht über den WebSocketManager.
        Wenn is_raw_crewai_output True ist, wird kein zusätzliches Präfix hinzugefügt.
        """
        if is_raw_crewai_output:
            formatted_message = content # Sende den rohen Output direkt
        else:
            formatted_message = f"{self._log_prefix_str} [{event_type}] {content}"
        
        await self.websocket_manager.send_log_to_task(self.task_id, formatted_message)
        logger.debug(f"{self._log_prefix_str} [WS Send] Event: '{event_type}', Raw: {is_raw_crewai_output}, Content (gekürzt): '{content[:100]}...'")

    # --- LLM Callbacks ---
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        invocation_params = kwargs.get("invocation_params", {}) # Korrekter Key-Zugriff
        # Versuche, den Modellnamen aus verschiedenen Quellen zu bekommen
        model_name_from_serialized = serialized.get("model_name") 
        model_name_from_invocation = invocation_params.get("model_name")
        model_id_list = serialized.get("id", [])
        model_name_from_id = model_id_list[-1] if isinstance(model_id_list, list) and model_id_list else "Unbekanntes LLM"
        
        model_name = model_name_from_invocation or model_name_from_serialized or model_name_from_id
        
        # Detailliertes Logging des vollständigen Prompts auf dem Server (siehe vorherige Empfehlung)
        full_prompts_str = "\n--- PROMPT SEPARATOR ---\n".join(prompts)
        inputs_kwarg = kwargs.get("inputs", {})
        detailed_server_log = (
            f"{self._log_prefix_str} [LLM Start - SERVER DEBUG]\n"
            f"  LLM Call ID (kwargs['run_id']): {kwargs.get('run_id')}\n"
            f"  Calling LLM: '{model_name}'\n"
            f"  Serialized 'id' (Chain/Agent): {serialized.get('id')}\n"
            f"  String Prompts (argument 'prompts'):\n{full_prompts_str}\n"
            f"  Structured Inputs (kwargs['inputs']): {inputs_kwarg}\n"
        )
        if isinstance(inputs_kwarg, dict) and "messages" in inputs_kwarg:
             actual_messages_sent = inputs_kwarg["messages"]
             detailed_server_log += f"  Actual List[BaseMessage] (from inputs['messages']):\n{actual_messages_sent}\n"
        detailed_server_log += "--- ENDE SERVER DEBUG PROMPT ---"
        logger.info(detailed_server_log)

        await self._send_log("LLM Start", f"Modell '{model_name}' wird mit {len(prompts)} Prompt(s) aufgerufen. Erster Prompt (gekürzt): '{prompts[0][:200]}...'") # Gekürzt für WS

    async def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        try:
            if hasattr(response, 'generations') and response.generations:
                first_generation_group = response.generations[0]
                if first_generation_group:
                    first_generation = first_generation_group[0]
                    if hasattr(first_generation, 'message') and hasattr(first_generation.message, 'content'):
                        output_summary = first_generation.message.content
                    elif hasattr(first_generation, 'text'):
                        output_summary = first_generation.text
                    else:
                        output_summary = str(response) # Fallback
                else:
                    output_summary = str(response) # Fallback
            else:
                output_summary = str(response) # Fallback
            await self._send_log("LLM Ende", f"Modellaufruf beendet. Antwort (gekürzt): '{output_summary[:200]}...'")
        except Exception as e:
            await self._send_log("LLM Ende", f"Modellaufruf beendet. Antwort konnte nicht vollständig extrahiert werden (Fehler: {e}). Antwort-Objekt (gekürzt): {str(response)[:200]}...")

    # --- Chain Callbacks ---
    async def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        chain_name = serialized.get("name", serialized.get("id", ["Unbekannte Kette"])[-1])
        input_keys = list(inputs.keys())
        await self._send_log("Kette Start", f"Kette '{chain_name}' gestartet. Input-Schlüssel: {input_keys}.")

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        chain_name = kwargs.get("name", "Unbekannte Kette") # CrewAI setzt hier oft den Agentennamen
        output_summary = str(outputs)[:300]
        await self._send_log("Kette Ende", f"Kette '{chain_name}' beendet. Output (gekürzt): '{output_summary}...'")

    # --- Tool Callbacks ---
    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        tool_name = serialized.get("name", "Unbekanntes Tool")
        await self._send_log("Tool Start", f"Tool '{tool_name}' wird ausgeführt mit Input (gekürzt): '{input_str[:200]}...'")

    async def on_tool_end(self, output: str, **kwargs: Any) -> None:
        tool_name = kwargs.get("name", "Unbekanntes Tool")
        agent_name = kwargs.get("agent_name", "") # Versuch, den Agentennamen zu bekommen
        log_source = f"{agent_name} - {tool_name}" if agent_name else tool_name
        await self._send_log(f"{log_source} Output", f"(gekürzt): '{str(output)[:200]}...'")

    async def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        tool_name = kwargs.get("name", "Unbekanntes Tool")
        await self._send_log("Tool Fehler", f"Fehler bei Ausführung von Tool '{tool_name}': {str(error)}")

    # --- Agent Specific Callbacks ---
    async def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
        agent_name = kwargs.get('name', 'Agent')
        
        # Gedanken des Agenten (oft in action.log)
        # Das `action.log` enthält oft die vollständige LLM-Antwort, die zum Tool-Aufruf geführt hat,
        # inklusive der "Thought:"-Kette.
        agent_thought_process = getattr(action, 'log', '').strip()
        if agent_thought_process:
            # Wir können versuchen, nur den relevanten Teil des Gedankens zu extrahieren oder alles zu senden.
            # Oft ist die "Thought:"-Zeile die erste Zeile oder ein signifikanter Teil.
            # Eine einfache heuristische Trennung, um nicht den ganzen Log-Block zu wiederholen:
            thought_lines = [line.strip() for line in agent_thought_process.split('\n') if line.strip()]
            relevant_thoughts = []
            capture_thought = False
            for line in thought_lines:
                if line.lower().startswith("thought:"):
                    relevant_thoughts.append(line[len("thought:"):].strip())
                    capture_thought = True # Erfasse auch folgende Zeilen bis zur nächsten Aktion
                elif capture_thought and not (line.lower().startswith("action:") or line.lower().startswith("action input:")):
                    relevant_thoughts.append(line)
                elif line.lower().startswith("action:") or line.lower().startswith("action input:"):
                    capture_thought = False # Stoppe Erfassung, wenn Aktionsdetails beginnen
            
            if relevant_thoughts:
                await self._send_log(f"{agent_name} Thought", " ".join(relevant_thoughts))

        # Geplante Aktion
        tool_name = action.tool
        tool_input_summary = str(action.tool_input)[:200] # Gekürzt für WebSocket
        await self._send_log(f"{agent_name} Action", f"Plant Tool '{tool_name}' mit Input (gekürzt): '{tool_input_summary}...'")
        # Logge auch den vollen Tool-Input auf dem Server für besseres Debugging
        logger.info(f"{self._log_prefix_str} [{agent_name} Action - SERVER DEBUG] Tool: '{tool_name}', Vollständiger Input: {action.tool_input}")


    async def on_agent_finish(self, finish: Any, **kwargs: Any) -> Any:
        agent_name = kwargs.get('name', 'Agent')
        output = finish.return_values.get("output", "")
        output_summary = str(output)[:200]
        await self._send_log(f"{agent_name} Abschluss", f"Schritt beendet. Output (gekürzt): '{output_summary}...'")

    # --- Generischer Text-Callback ---
    async def on_text(self, text: str, **kwargs: Any) -> None:
        if text and text.strip():
            source_name = kwargs.get('name', 'System/Agent')
            # Vermeide das Loggen von "Thought:", wenn es bereits von on_agent_action abgedeckt wird.
            if not text.lower().strip().startswith("thought:"):
                await self._send_log(f"{source_name} Info", text.strip())

class WebSocketStream(io.StringIO):
    def __init__(
        self,
        callback_handler: WebSocketCallbackHandler,
        original_stdout: Any,
        event_type_prefix: str = "CrewAI Console",
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        super().__init__()
        self.callback_handler = callback_handler
        self.original_stdout = original_stdout  # Speichere das originale stdout
        self.event_type_prefix = event_type_prefix
        self.line_buffer = ""  # Puffer für Zeilen
        self.loop = loop or asyncio.get_event_loop()

    def _schedule_send(self, coro: asyncio.Future) -> None:
        """Sende das Log sicher im Hauptloop, auch wenn write() aus einem Thread
        aufgerufen wird."""
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(asyncio.create_task, coro)
        else:
            asyncio.run(coro)

    def write(self, s: str) -> int:
        # Schreibe auch in das originale stdout, damit es weiterhin in der Server-Konsole erscheint
        self.original_stdout.write(s)
        self.original_stdout.flush()

        # Füge zum Puffer hinzu und sende ganze Zeilen
        self.line_buffer += s
        if '\n' in self.line_buffer:
            lines = self.line_buffer.split('\n')
            self.line_buffer = lines[-1]  # Behalte den Rest für die nächste Zeile
            for line in lines[:-1]:
                if line.strip():  # Sende keine leeren Zeilen
                    self._schedule_send(
                        self.callback_handler._send_log(
                            self.event_type_prefix,
                            line.strip(),
                            is_raw_crewai_output=True,
                        )
                    )
        return len(s)

    def flush(self) -> None:
        self.original_stdout.flush()
        # Sende verbleibenden Pufferinhalt, falls vorhanden und nicht mit Newline endet
        if self.line_buffer.strip():
            self._schedule_send(
                self.callback_handler._send_log(
                    self.event_type_prefix,
                    self.line_buffer.strip(),
                    is_raw_crewai_output=True,
                )
            )
            self.line_buffer = ""