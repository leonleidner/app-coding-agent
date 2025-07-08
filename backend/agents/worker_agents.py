# coding_agent_backend/agents/worker_agents.py
from crewai import Agent
from llm_config import default_llm # Nutzen das Standard-LLM
from tools import python_repl, load_dataset, analyze_csv, custom_csv_search_tool, summarize_csv_tool, notebook_writer_tool# Importiere die benötigten Tools

class WorkerAgents():
    # 1. Data Gatherer Agent
    def data_gatherer(self, dataset_path: str):
        return Agent(
            role='Data Acquisition Specialist',
            goal="Sammle, validiere und dokumentiere die Daten aus der bereitgestellten CSV-Datei '{dataset_path}' für das Projekt '{project_goal}'. Beschreibung: {dataset_description}",
            backstory="Als Datensammler-Experte bist du darauf spezialisiert, relevante und qualitativ hochwertige Daten zu identifizieren und zu beschaffen. Du kennst dich mit verschiedenen Datenquellen aus und stellst sicher, dass die Datenbasis für die Analyse vollständig und korrekt ist.",
            llm=default_llm,
            tools=[custom_csv_search_tool, load_dataset],
            allow_delegation=True,
            verbose=True
        )

    # 2. Data Cleaning & Preprocessing Agent
    def data_cleaner(self): 
        return Agent(
            role='Data Preparation Engineer',
            goal="Bereinige und transformiere die Rohdaten ({input_data_summary}) sorgfältig, um sie für die nachfolgende Analyse und Modellierung im Rahmen des Projekts '{project_goal}' optimal vorzubereiten. Konzentriere dich auf fehlende Werte, Datentypen, Duplikate und Ausreißer.",
            backstory="Du bist ein Detail-orientierter Ingenieur für Datenaufbereitung. Deine Aufgabe ist es, aus unstrukturierten Rohdaten einen sauberen, konsistenten und zuverlässigen Datensatz zu erstellen, der als solide Grundlage für alle weiteren Data-Science-Schritte dient.",
            llm=default_llm,
            tools=[summarize_csv_tool],
            allow_delegation=True,
            verbose=True
        )

    # 3. Exploratory Data Analysis (EDA) Agent
    def eda_agent(self):
        return Agent(
            role='Exploratory Data Analyst',
            goal="Führe eine tiefgreifende explorative Datenanalyse der vorbereiteten Daten ({cleaned_data_summary}) durch. Identifiziere Muster, Trends, Korrelationen und Anomalien. Erstelle aussagekräftige Visualisierungen und formuliere erste Hypothesen für das Projekt '{project_goal}'.",
            backstory="Mit deiner analytischen Schärfe und deinem Gespür für Datenmuster deckst du verborgene Einsichten auf. Du verwandelst Zahlen in Geschichten und bereitest den Weg für fundierte Modellentscheidungen.",
            llm=default_llm,
            tools=[notebook_writer_tool, summarize_csv_tool],
            allow_delegation=True,
            verbose=True
        )

    # 4. Modeling & Evaluation Agent
    def modeling_agent(self):
        return Agent(
            role='Machine Learning Engineer',
            goal="Entwickle, trainiere und evaluiere prädiktive Modelle basierend auf den EDA-Erkenntnissen ({eda_insights}) und den bereinigten Daten ({cleaned_data_summary}), um das Kernziel des Projekts '{project_goal}' zu erreichen. Wähle das robusteste und leistungsfähigste Modell aus und dokumentiere dessen Performance.",
            backstory="Als Machine Learning Experte beherrschst du ein breites Spektrum an Algorithmen und Optimierungstechniken. Dein Ziel ist es, Modelle zu bauen, die nicht nur präzise, sondern auch interpretierbar und zuverlässig sind.",
            llm=default_llm,
            tools=[notebook_writer_tool],
            allow_delegation=False,
            verbose=True
        )

    # 5. Reporting & Insights Agent
    def reporting_agent(self):
        return Agent(
            role='Data Insights Communicator',
            goal="Nutze das Tool 'Search a CSV's content' um die CSV Datei einzulesen, dann Nutze das Tool 'Write code to Jupyter Notebook', um den Code in eine `.ipynb` Datei zu schreiben. Speichere das Notebook als neue Datei unter: /Users/leonleidner/app-coding-agent/backend/notebooks/. Führe den Code NICHT aus. Liefere keinen eigenen Code oder Text zurück – nutze ausschließlich das Tool. Achte darauf, dass ein String nicht zu Float konvertiert werden kann. Diese Spalte muss dann ausgelassen werden.",
            backstory="Du bist ein Meister darin, komplexe technische Informationen und Datenerkenntnisse in eine klare, prägnante und für Stakeholder zugängliche Sprache zu übersetzen. Deine Berichte sind nicht nur informativ, sondern inspirieren auch zu datenbasierten Entscheidungen. Arbeite mit Seaborn, Pandas usw. um die Datenerkenntnisse anschaulich darzustellen.",
            llm=default_llm,
            tools=[notebook_writer_tool, custom_csv_search_tool], # Kann für das Formatieren von Markdown-Tabellen etc. nützlich sein
            allow_delegation=False,
            verbose=True
        )