import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class OpenAIConfig:
    API_KEY = os.getenv("GITHUB_TOKEN")
    ENDPOINT = os.getenv("LLM_ENDPOINT")
    CONSULTANT_MODEL = "meta/Meta-Llama-3.1-70B-Instruct"
    NUTRITIONIST_MODEL = "openai/gpt-4.1-mini"
    SEARCHER_MODEL = "openai/gpt-4.1-mini"
    EMBEDDING_MODEL = "text-embedding-3-small"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1