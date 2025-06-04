from crewai import Task
from agents import lead_data_scientist # Importiere den Manager-Agenten, dem der Task zugewiesen wird

# Haupt-Projekttask
data_science_project_task = Task(
    description=(
        "Führe ein vollständiges Data-Science-Projekt durch. "
        "Projektziel: {user_project_goal}. "
        "Verwendeter Datensatz/Beschreibung: {user_dataset_description}. "
        "Ursprüngliche Benutzeranfrage: {user_raw_query}. "
        "Das Projekt umfasst Datensammlung, -bereinigung, explorative Datenanalyse (EDA), "
        "Modellentwicklung und -evaluierung sowie die Erstellung eines detaillierten Abschlussberichts."
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
    agent=lead_data_scientist # Dieser Task wird dem Manager-Agenten zugewiesen
)