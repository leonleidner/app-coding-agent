from crewai import Agent
from llm_config import manager_llm
from .worker_agents import WorkerAgents # Importiere die Worker-Instanzen

class managerAgent():
    def lead_data_scientist(self):
        return Agent(
            role='Project Manager',
            goal=(
                "Koordiniere und leite ein Team von KI-Spezialisten, um das Data-Science-Projekt '{project_goal}' "
                "mit dem Datensatz '{dataset_path}' erfolgreich abzuschließen. Zerlege die Hauptaufgabe in "
                "Teilaufgaben, delegiere diese an geeignete Coworker (z.B. Data Insights Communicator), "
                "überwache den Fortschritt, fasse die Ergebnisse zusammen und dokumentiere den Projektabschluss. "
                "Die Coworker dürfen Tools verwenden, um ihre Aufgaben umzusetzen (z.B. Python in Jupyter Notebooks schreiben)."
            ),
            backstory=(
                "Du bist ein erfahrener Projektmanager im Bereich Data Science. Dein Team besteht aus:\n"
                "- Data Insights Communicator\n"
                "Du leitest das Team, delegierst Aufgaben, koordinierst Ergebnisse und lieferst ein Gesamtergebnis. "
                "Führe keine Aufgaben selbst aus – arbeite ausschließlich durch Koordination und Delegation."
            ),
            llm=manager_llm,
            allow_delegation=False,
            verbose=True,
            max_iter=15
        )