import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import traceback

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Das Modell, das als manager_llm konfiguriert ist (oder ein anderes zum Testen)
MODEL_NAME = "gemini-1.5-flash"
# MODEL_NAME = "gemini-pro" # Alternativ zum Testen

print(f"Versuche Verbindung mit Google Gemini:")
print(f"  API Key (erste 5 Zeichen): {GOOGLE_API_KEY[:5] if GOOGLE_API_KEY else 'NICHT GESETZT'}")
print(f"  Modell: {MODEL_NAME}")

if not GOOGLE_API_KEY:
    print("FEHLER: GOOGLE_API_KEY nicht in .env gefunden oder nicht gesetzt.")
else:
    try:
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1,
            convert_system_message_to_human=True # Wichtig für Gemini
        )
        print(f"\nChatGoogleGenerativeAI-Instanz für {MODEL_NAME} erstellt. Sende Test-Prompt...")

        response = llm.invoke("Führe ein vollständiges Data-Science-Projekt durch. Projektziel: Allgemeine Analyse durchführen. Verwendeter Datensatz/Beschreibung: Keine spezifische Dataset-Beschreibung angegeben. Ursprüngliche Benutzeranfrage: Analysiere mein Dataset. Das Projekt umfasst Datensammlung, -bereinigung,explorative Datenanalyse (EDA), Modellentwicklung und -evaluierung sowie die Erstellung eines detaillierten Abschlussberichts.") # Einfacher Test-Prompt

        print("\nAntwort vom LLM (Gemini):")
        if hasattr(response, 'content'):
            print(response.content)
        else:
            print(response) # Falls die Struktur anders ist

    except Exception as e:
        print(f"\nFEHLER beim Testen des Gemini LLMs ({MODEL_NAME}): {e}")
        print("------------------- Traceback -------------------")
        traceback.print_exc()
        print("-------------------------------------------------")
        print("Mögliche Gründe: API Key ungültig/falsche Berechtigungen, Modell nicht verfügbar/falsch geschrieben,")
        print("Netzwerkproblem, Google API Problem, oder Problem mit der langchain-google-genai Bibliothek.")