# coding_agent_backend/agents/__init__.py
from .manager_agent import lead_data_scientist
from .worker_agents import data_gatherer, data_cleaner, eda_agent, modeling_agent, reporting_agent, all_worker_agents

# Liste aller Agenten für die Crew-Erstellung
list_of_all_agents = [lead_data_scientist] + all_worker_agents
all_worker_agents = all_worker_agents