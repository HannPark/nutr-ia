import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class OpenAIConfig:
    API_KEY = os.getenv("GITHUB_TOKEN")
    ENDPOINT = "https://models.github.ai/inference"
    CONSULTANT_MODEL = "meta/Llama-4-Maverick-17B-128E-Instruct-FP8"
    NUTRITIONIST_MODEL = "openai/gpt-4.1"
    SEARCHER_MODEL = "openai/gpt-4.1"
    EMBEDDING_MODEL = "text-embedding-3-small"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1