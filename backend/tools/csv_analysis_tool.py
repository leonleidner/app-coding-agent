from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Any
import pandas as pd

class CSVAnalysisToolInput(BaseModel):
    """Input schema for CSVAnalysisTool"""
    file_path: str = Field(..., description="Path to the CSV file")

class CSVAnalysisTool(BaseTool):
    name: str = "CSV Analysis Tool"
    description: str = (
        "Loads a CSV file from a given path and returns a brief summary "
        "including shape and basic statistics."
    )
    args_schema: Type[BaseModel] = CSVAnalysisToolInput

    def _run(self, file_path: str, **kwargs: Any) -> str:
        try:
            df = pd.read_csv(file_path)
            summary = df.describe(include='all').to_string()
            shape = df.shape
            return (
                f"Dataset loaded from {file_path}. Shape: {shape[0]} rows, {shape[1]} columns.\n"
                f"Summary statistics:\n{summary}"
            )
        except Exception as e:
            return f"ERROR loading dataset {file_path}: {e}"

    async def _arun(self, file_path: str, **kwargs: Any) -> str:
        return self._run(file_path, **kwargs)

analyze_csv = CSVAnalysisTool()
