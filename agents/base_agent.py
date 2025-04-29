import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
from config.openai_config import OpenAIConfig

class BaseAgent:
    def __init__(self, name, model_name):
        self.name = name
        self.model_name = model_name
        self.kernel = sk.Kernel()
        self._setup_kernel()
        
    def _setup_kernel(self):
        # Configurar el Semantic Kernel con OpenAI
        api_key = OpenAIConfig.API_KEY
        self.kernel.add_chat_service(
            service_id=self.name,
            service=OpenAIChatCompletion(
                model_id=self.model_name,
                api_key=api_key
            )
        )
        self.kernel.add_text_embedding_generation_service(
            service_id="embedding",
            service=OpenAITextEmbedding(
                model_id=OpenAIConfig.EMBEDDING_MODEL,
                api_key=api_key
            )
        )
    
    def load_skills(self, skills_dir=None,native=None):
        
        skills = {}

        if skills_dir:
            semantic_skills = self.kernel.import_semantic_skill_from_directory(skills_dir, self.name)
            skills.update(semantic_skills)

        if native:
            print(native)
            for name, skill_instance in native.items():
                imported_skill = self.kernel.import_skill(skill_instance, name)
                skills.update(imported_skill)

        print(skills)

        return skills
        
    async def process(self, input_data):
        # Método a implementar en clases derivadas
        raise NotImplementedError("Este método debe ser implementado por las subclases")
