# coding_agent_backend/llm_config.py
from crewai import LLM
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

google_api_key = os.getenv("GOOGLE_API_KEY")

#openrouter_api_base = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")

# Standard LLM für die Worker-Agenten, konfiguriert für OpenRouter
default_llm = LLM(
    model="openrouter/deepseek/deepseek-chat-v3-0324:free",
    api_key=os.environ['OPENAI_API_KEY'],
    temperature=0.3,
)

# LLM für den Manager der Crew, konfiguriert für OpenRouter
manager_llm = LLM(
    model="openrouter/deepseek/deepseek-chat-v3-0324:free",
    api_key=os.environ['OPENAI_API_KEY'],
    temperature=0.1,
)

print(f"LLM Config: Default model - {default_llm.model}")
print(f"LLM Config: Manager model - {manager_llm.model}")