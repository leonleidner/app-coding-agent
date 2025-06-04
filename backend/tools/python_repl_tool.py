# coding_agent_backend/tools/python_repl_tool.py
from crewai.tools import BaseTool # Wichtig: Import von crewai.tools
from langchain_experimental.tools import PythonREPLTool as LangchainPythonREPLTool # Umbenannt für Klarheit
from pydantic import BaseModel, Field
from typing import Type, Any

# Definiere das Schema für die Eingabeargumente
class PythonREPLToolInput(BaseModel):
    """Input schema for the Python REPL Tool."""
    command: str = Field(..., description="Der Python-Code, der im REPL ausgeführt werden soll.")

class CustomPythonREPLTool(BaseTool):
    name: str = "Python Code Executor"
    description: str = (
        "Ein Python REPL (Read-Eval-Print Loop). Führt Python-Code aus und gibt das Ergebnis (stdout, stderr oder Rückgabewert) zurück. "
        "Sehr nützlich für Datenmanipulation mit Pandas, mathematische Berechnungen mit NumPy, "
        "oder jede andere Aufgabe, die durch Ausführen von Python-Code gelöst werden kann. "
        "Achtung: Code wird direkt ausgeführt!"
    )
    args_schema: Type[BaseModel] = PythonREPLToolInput
    _langchain_repl: LangchainPythonREPLTool # Interne Instanz des originalen Tools

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._langchain_repl = LangchainPythonREPLTool() # Initialisiere das Original-Tool hier

    def _run(self, command: str, **kwargs: Any) -> str:
        """Führt den Python-Befehl aus."""
        # WICHTIG: Sicherheitshinweis bleibt bestehen!
        # Die Ausführung von beliebigem Code ist ein erhebliches Sicherheitsrisiko.
        # In einer Produktivumgebung sind strikte Sandbox-Mechanismen unerlässlich.
        try:
            return self._langchain_repl.run(command)
        except Exception as e:
            return f"Fehler bei der Ausführung des Python-Codes: {str(e)}"

# Instanziiere dein benutzerdefiniertes Tool
python_repl = CustomPythonREPLTool()