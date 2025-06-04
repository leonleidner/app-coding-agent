# coding_agent_backend/agents/worker_agents.py
from crewai import Agent
from llm_config import default_llm # Nutzen das Standard-LLM
from tools import python_repl, load_dataset # Importiere die benötigten Tools

# 1. Data Gatherer Agent
data_gatherer = Agent(
    role='Data Acquisition Specialist',
    goal="Sammle, validiere und dokumentiere alle notwendigen Daten aus den spezifizierten Quellen für das Projekt '{project_goal}' unter Verwendung des Datensatzes '{dataset_description}'.",
    backstory="Als Datensammler-Experte bist du darauf spezialisiert, relevante und qualitativ hochwertige Daten zu identifizieren und zu beschaffen. Du kennst dich mit verschiedenen Datenquellen aus und stellst sicher, dass die Datenbasis für die Analyse vollständig und korrekt ist.",
    llm=default_llm,
    tools=[load_dataset], # Beispiel-Tool
    allow_delegation=False,
    verbose=True
)

# 2. Data Cleaning & Preprocessing Agent
data_cleaner = Agent(
    role='Data Preparation Engineer',
    goal="Bereinige und transformiere die Rohdaten ({input_data_summary}) sorgfältig, um sie für die nachfolgende Analyse und Modellierung im Rahmen des Projekts '{project_goal}' optimal vorzubereiten. Konzentriere dich auf fehlende Werte, Datentypen, Duplikate und Ausreißer.",
    backstory="Du bist ein Detail-orientierter Ingenieur für Datenaufbereitung. Deine Aufgabe ist es, aus unstrukturierten Rohdaten einen sauberen, konsistenten und zuverlässigen Datensatz zu erstellen, der als solide Grundlage für alle weiteren Data-Science-Schritte dient.",
    llm=default_llm,
    tools=[python_repl],
    allow_delegation=False,
    verbose=True
)

# 3. Exploratory Data Analysis (EDA) Agent
eda_agent = Agent(
    role='Exploratory Data Analyst',
    goal="Führe eine tiefgreifende explorative Datenanalyse der vorbereiteten Daten ({cleaned_data_summary}) durch. Identifiziere Muster, Trends, Korrelationen und Anomalien. Erstelle aussagekräftige Visualisierungen und formuliere erste Hypothesen für das Projekt '{project_goal}'.",
    backstory="Mit deiner analytischen Schärfe und deinem Gespür für Datenmuster deckst du verborgene Einsichten auf. Du verwandelst Zahlen in Geschichten und bereitest den Weg für fundierte Modellentscheidungen.",
    llm=default_llm,
    tools=[python_repl],
    allow_delegation=False,
    verbose=True
)

# 4. Modeling & Evaluation Agent
modeling_agent = Agent(
    role='Machine Learning Engineer',
    goal="Entwickle, trainiere und evaluiere prädiktive Modelle basierend auf den EDA-Erkenntnissen ({eda_insights}) und den bereinigten Daten ({cleaned_data_summary}), um das Kernziel des Projekts '{project_goal}' zu erreichen. Wähle das robusteste und leistungsfähigste Modell aus und dokumentiere dessen Performance.",
    backstory="Als Machine Learning Experte beherrschst du ein breites Spektrum an Algorithmen und Optimierungstechniken. Dein Ziel ist es, Modelle zu bauen, die nicht nur präzise, sondern auch interpretierbar und zuverlässig sind.",
    llm=default_llm,
    tools=[python_repl],
    allow_delegation=False,
    verbose=True
)

# 5. Reporting & Insights Agent
reporting_agent = Agent(
    role='Data Insights Communicator',
    goal="Erstelle einen umfassenden, aber verständlichen Bericht, der alle Phasen des Data-Science-Projekts '{project_goal}' zusammenfasst: von der Datensammlung ({gathered_data_summary}) über die Bereinigung ({cleaned_data_summary}) und EDA ({eda_insights}) bis hin zur Modellierung ({model_details_and_performance}). Leite klare Handlungsempfehlungen ab.",
    backstory="Du bist ein Meister darin, komplexe technische Informationen und Datenerkenntnisse in eine klare, prägnante und für Stakeholder zugängliche Sprache zu übersetzen. Deine Berichte sind nicht nur informativ, sondern inspirieren auch zu datenbasierten Entscheidungen.",
    llm=default_llm,
    tools=[python_repl], # Kann für das Formatieren von Markdown-Tabellen etc. nützlich sein
    allow_delegation=False,
    verbose=True
)

# Sammle alle Worker-Agenten für den einfachen Import
all_worker_agents = [
    data_gatherer,
    data_cleaner,
    eda_agent,
    modeling_agent,
    reporting_agent
]