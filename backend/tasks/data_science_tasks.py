from crewai import Task
from agents import manager_agent # Importiere den Manager-Agenten, dem der Task zugewiesen wird
from agents import WorkerAgents

# Haupt-Projekttask
class data_science_tasks():
    def data_science_project_task(self, agent):
        return Task(
            description=(
                "Projektziel: {user_project_goal}. "
                "Verwendeter Datensatz: {dataset_path}. "
                "Ursprüngliche Benutzeranfrage: {user_raw_query}. "
                "Erstelle einen Plan für den 'Data Insights Communicator' Agent, welcher dann ein Reporting in einer .ipynb Datei schreibt."
            ),
            expected_output=(
                "Ein umfassender Plan, was der 'Data Insights Communicator' Agent machen soll:\n"
                "1. Zusammenfassung der Aufgabenstellung und der verwendeten Daten.\n"
                "2. Detaillierte Beschreibung des Datasets mit visueller Darstellung. \n"
                "3. Beantwortung der ursprünglichen Fragestellung basierend auf der Analyse.\n"
                "4. Konkrete Handlungsempfehlungen (falls zutreffend)."
            ),
            agent=agent
        )
    def data_gather_task(self, agent, context): 
        return Task(
            description=(
                "Durchsuche die bereitgestellte CSV-Datei {dataset_path} nach relevanten Spalten "
                "und erkenne mögliche Datenanomalien. Verfasse eine kurze Zusammenfassung der "
                "gesammelten Daten inklusive Datenmenge, Spaltentypen und potenziellen Datenlücken."
            ),
            expected_output="Eine Zusammenfassung der gesammelten Daten unter dem Schlüssel {gathered_data_summary}",
            agent=agent,
            context=context
        )


    def data_clean_task(self, agent, context):
        return Task(
            description=(
                "Bereinige die Rohdaten basierend auf {gathered_data_summary}. Entferne oder impute "
                "fehlende Werte, korrigiere Datentypen, eliminiere Duplikate und markiere Ausreißer."
            ),
            expected_output="Einen Bericht der Bereinigungsschritte unter {cleaned_data_summary}",
            agent=agent,
            context=context
        )


    def eda_task(self, agent, context):
        return Task(
            description=(
                "Analysiere die bereinigten Daten gemäß {cleaned_data_summary}. Untersuche Verteilungen, "
                "Korrelationen und auffällige Muster. Erstelle Visualisierungen und formuliere Hypothesen."
            ),
            expected_output="Zusammenfassung der Erkenntnisse unter {eda_insights}",
            agent=agent,
            context=context
        )


    def modeling_task(self, agent, context):
        return Task(
            description=(
                "Nutze die Erkenntnisse aus {eda_insights} und die bereinigten Daten aus {cleaned_data_summary} "
                "um Modelle zu entwickeln und zu evaluieren. Dokumentiere das beste Modell und seine Performance."
            ),
            expected_output="Details zum besten Modell unter {model_details_and_performance}",
            agent=agent,
            context=context
        )


    def reporting_task(self, agent, context):
        return Task(
            description=(
                "Erstelle einen umfassenden Bericht basierend auf der bereitgestellte CSV-Datei {dataset_path}. Fasse alle Schritte zusammen und leite "
                "Handlungsempfehlungen ab. Benutze panads und seaborn, um die Daten schön darzustellen. Benutze dein Tool dafür."
            ),
            expected_output="Fertig formatierter Abschlussbericht im Markdown-Format als ipynb Datei. Mit python (panads und seaborn). Der Code soll ausführar sein.",
            agent=agent,
            context=context
        )