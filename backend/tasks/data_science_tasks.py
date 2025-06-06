from crewai import Task
from agents import manager_agent # Importiere den Manager-Agenten, dem der Task zugewiesen wird
from agents import WorkerAgents

# Haupt-Projekttask
class data_science_tasks():
    def data_science_project_task(self, agent):
        return Task(
            description=(
                "Führe ein vollständiges Data-Science-Projekt durch. "
                "Projektziel: {user_project_goal}. "
                "Verwendeter Datensatz: {dataset_path}. "
                "Ursprüngliche Benutzeranfrage: {user_raw_query}. "
                "Das Projekt umfasst Datensammlung, -bereinigung, explorative Datenanalyse (EDA), "
                "Modellentwicklung und -evaluierung sowie die Erstellung eines detaillierten Abschlussberichts."
                "Benutze die verschiedenen Coworker Agenten, die dir zu verfügung stehen."
            ),
            expected_output=(
                "Ein umfassender Abschlussbericht im Markdown-Format. Dieser Bericht soll beinhalten:\n"
                "1. Zusammenfassung der Aufgabenstellung und der verwendeten Daten.\n"
                "2. Detaillierte Beschreibung der Datenbereinigungsschritte.\n"
                "3. Wichtigste Erkenntnisse und Visualisierungen aus der EDA.\n"
                "4. Beschreibung des entwickelten Modells (Typ, Parameter, verwendete Features).\n"
                "5. Evaluationsmetriken des Modells und Interpretation der Ergebnisse.\n"
                "6. Beantwortung der ursprünglichen Fragestellung basierend auf der Analyse.\n"
                "7. Konkrete Handlungsempfehlungen (falls zutreffend)."
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
                "Erstelle einen umfassenden Bericht basierend auf {gathered_data_summary}, {cleaned_data_summary}, "
                "{eda_insights} und {model_details_and_performance}. Fasse alle Schritte zusammen und leite "
                "Handlungsempfehlungen ab."
            ),
            expected_output="Fertig formatierter Abschlussbericht im Markdown-Format",
            agent=agent,
            context=context
        )