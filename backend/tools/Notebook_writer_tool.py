from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import nbformat
from nbformat.v4 import new_notebook, new_code_cell

class NotebookWriterInput(BaseModel):
    code: str = Field(..., description="Python code to insert into the notebook")
    filename: str = Field(..., description="Filename of the notebook to write (e.g. analysis.ipynb)")

class NotebookWriterTool(BaseTool):
    name: str = "Write code to Jupyter Notebook"
    description: str = "Speichert den gegebenen Python-Code in einer neuen Jupyter Notebook Datei (ohne Ausführung)."
    args_schema: Type[BaseModel] = NotebookWriterInput

    def _run(self, code: str, filename: str, **kwargs) -> str:
        try:
            nb = new_notebook(cells=[new_code_cell(code)])
            with open(filename, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)
            return f"Notebook erfolgreich gespeichert unter: {filename}"
        except Exception as e:
            return f"Fehler beim Schreiben der Notebook-Datei: {e}"

    async def _arun(self, **kwargs):
        return self._run(**kwargs)

notebook_writer_tool = NotebookWriterTool()
