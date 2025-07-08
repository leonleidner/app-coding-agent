from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import pandas as pd

class SummarizeCSVToolInput(BaseModel):
    csv: str = Field(..., description="Pfad zur CSV-Datei, die zusammengefasst werden soll")

class SummarizeCSVTool(BaseTool):
    name: str = "Summarize a CSV"
    description: str = "Lädt eine CSV-Datei und gibt eine strukturierte Zusammenfassung (Spalten, Datentypen, Nullwerte, Statistik) zurück."
    args_schema: Type[BaseModel] = SummarizeCSVToolInput

    def _run(self, csv: str, **kwargs) -> str:
        try:
            df = pd.read_csv(csv)

            info = f"📊 CSV-Zusammenfassung für Datei: {csv}\n"
            info += f"• Form: {df.shape[0]} Zeilen, {df.shape[1]} Spalten\n"
            info += "\n• Spaltenübersicht:\n"
            info += "\n".join([f"  - {col} ({dtype})" for col, dtype in df.dtypes.items()])

            nulls = df.isnull().sum()
            null_summary = "\n".join([f"  - {col}: {count} fehlende Werte" for col, count in nulls.items() if count > 0])
            if null_summary:
                info += "\n\n• Fehlende Werte:\n" + null_summary
            else:
                info += "\n\n• Keine fehlenden Werte gefunden."

            numeric_summary = df.describe(include='number').to_string()
            info += f"\n\n• Statistische Übersicht (nur numerische Spalten):\n{numeric_summary}"

            return info
        except Exception as e:
            raise Exception(f"Fehler beim Verarbeiten der CSV-Datei '{csv}': {str(e)}")


    async def _arun(self, csv: str, **kwargs) -> str:
        return self._run(csv, **kwargs)

summarize_csv_tool = SummarizeCSVTool()
