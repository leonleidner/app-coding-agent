# coding_agent_backend/tools/custom_ds_tools.py
from crewai.tools import BaseTool # Wichtig: Import von crewai.tools
from pydantic import BaseModel, Field
from typing import Type, Any # Type wird für args_schema benötigt

# Definiere das Schema für die Eingabeargumente deines Tools
class LoadDatasetToolInput(BaseModel):
    """Input schema for LoadDatasetTool."""
    dataset_name: str = Field(..., description="Der Name des zu ladenden Datensatzes, z.B. 'titanic' oder 'iris'.")

class LoadDatasetTool(BaseTool):
    name: str = "Dataset Loader Tool" # Name des Tools
    description: str = ( # Beschreibung, die das LLM sieht
        "Nützlich, um Informationen über einen bekannten Datensatz basierend auf seinem Namen abzurufen oder dessen Laden zu simulieren. "
        "Gibt eine Erfolgs- oder Fehlermeldung als String zurück, die den Status beschreibt. "
        "Beispiel-Datensätze: 'titanic', 'iris', 'customer_data_q1'."
    )
    args_schema: Type[BaseModel] = LoadDatasetToolInput # Verknüpfung mit dem Input-Schema

    def _run(self, dataset_name: str, **kwargs: Any) -> str:
        """Führt die Tool-Logik aus (synchrone Version)."""
        # Hier deine Logik zum Laden von Daten.
        # Wichtig: Dieses Tool sollte einen String zurückgeben.
        # Wenn du DataFrames laden willst, die später im PythonREPLTool verwendet werden,
        # könntest du hier einen Pfad oder eine Bestätigung zurückgeben, dass die Daten
        # in einer bestimmten Variable im REPL-Kontext verfügbar sind (erfordert mehr Logik).
        # Fürs Erste simulieren wir das Abrufen von Infos.

        if dataset_name.lower() == "titanic":
            return f"INFO: Titanic dataset (1309 Zeilen, 14 Spalten) Informationen abgerufen. Simulierte Verfügbarkeit unter '/data/titanic.csv'."
        elif dataset_name.lower() == "customer_data_q1":
            return f"INFO: Dataset '{dataset_name}' (Beispiel: 5000 Zeilen, 25 Spalten) Informationen abgerufen (simuliert)."
        else:
            return f"FEHLER: Dataset '{dataset_name}' konnte nicht gefunden oder geladen werden."

    async def _arun(self, dataset_name: str, **kwargs: Any) -> str:
        """Führt die Tool-Logik asynchron aus (optional, aber gute Praxis)."""
        # Für dieses einfache Tool können wir die synchrone Methode aufrufen.
        # Bei echten I/O-Operationen würdest du hier `asyncio` verwenden.
        return self._run(dataset_name=dataset_name)

# Instanziiere dein Tool, damit du es leicht importieren kannst
load_dataset = LoadDatasetTool()