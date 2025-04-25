import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class OpenAIConfig:
    API_KEY = os.getenv("GITHUB_TOKEN")
    CONSULTANT_MODEL = "gpt-4"
    NUTRITIONIST_MODEL = "gpt-4"
    SEARCHER_MODEL = "gpt-3.5-turbo"
    EMBEDDING_MODEL = "text-embedding-3-small"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7