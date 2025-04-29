import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class OpenAIConfig:
    API_KEY = os.getenv("GITHUB_TOKEN")
    ENDPOINT = "https://models.inference.ai.azure.com"
    CONSULTANT_MODEL = "gpt-4o"
    NUTRITIONIST_MODEL = "gpt-4o"
    SEARCHER_MODEL = "gpt-4o-mini"
    EMBEDDING_MODEL = "text-embedding-3-small"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1