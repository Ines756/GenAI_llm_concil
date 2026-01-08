"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()


# Council members - list of model identifiers
COUNCIL_MODELS = [
    "gemma2:2b",  # Noms de modèles Ollama (sans le préfixe ollama/)
    "llama3.2:latest",
    "smollm2:135m"

]

# Chairman model - synthesizes final response
# Using a larger model for better synthesis capability
CHAIRMAN_MODEL = "mistral:latest"

# API endpoints - configurable for distributed setup
# Format: {"model_name": "http://ip:port"}
OLLAMA_ENDPOINTS = {
    "gemma2:2b": os.getenv("OLLAMA_ENDPOINT_1", "http://localhost:11434"),
    "llama3.2:latest": os.getenv("OLLAMA_ENDPOINT_2", "http://localhost:11434"),
    "mistral:latest": os.getenv("OLLAMA_CHAIRMAN", "http://localhost:11434"),
    "smollm2:135m": os.getenv("OLLAMA_ENDPOINT_3", "http://localhost:11434"),
    # Chairman endpoint added automatically for mistral:latest
}

# Ollama API path (same for all endpoints)
OLLAMA_API_PATH = "/api/chat"  # ou "/api/generate" selon ce que tu utilises

# Data directory for conversation storage
DATA_DIR = "data/conversations"