from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import pandas as pd

class CSVSearchToolInput(BaseModel):
    search_query: str = Field(..., description="Suchbegriff oder Ausdruck, der in der CSV gesucht werden soll")
    csv: str = Field(..., description="Pfad zur CSV-Datei, in der gesucht werden soll")

class CustomCSVSearchTool(BaseTool):
    name: str = "Search a CSV's content"
    description: str = "Durchsucht eine CSV-Datei nach einem bestimmten Suchbegriff in allen Spalten."
    args_schema: Type[BaseModel] = CSVSearchToolInput

    def _run(self, search_query: str, csv: str, **kwargs) -> str:
        try:
            df = pd.read_csv(csv)
            matches = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)]
            if matches.empty:
                return f"Keine Übereinstimmungen für '{search_query}' in Datei {csv} gefunden."
            return f"Gefundene Zeilen:{matches.to_string(index=False)}"
        except Exception as e:
            raise Exception(f"Fehler beim Verarbeiten der CSV-Datei '{csv}': {str(e)}")


    async def _arun(self, search_query: str, csv: str, **kwargs) -> str:
        return self._run(search_query, csv, **kwargs)

custom_csv_search_tool = CustomCSVSearchTool()
