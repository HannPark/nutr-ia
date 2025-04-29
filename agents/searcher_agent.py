import json
import semantic_kernel as sk
from config.openai_config import OpenAIConfig
from .base_agent import BaseAgent
from skills.searcher.search_recipes import SearchRecipeSkill
from skills.searcher.search_videos import SearchVideosSkill

class SearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("searcher", OpenAIConfig.SEARCHER_MODEL)
        self.skills = self.load_skills("skills/searcher_skills")
    
    async def find_recipes(self, diet_type, restrictions):
        # Buscar recetas apropiadas
        context = sk.ContextVariables()
        context["diet_type"] = diet_type
        context["restrictions"] = json.dumps(restrictions)
        
        result = await self.kernel.run_async(
            self.skills["search_recipes"],
            input_vars=context
        )
        
        recipes = json.loads(result)
        return recipes
    
    async def find_videos(self, condition, diet_type):
        # Buscar videos informativos
        context = sk.ContextVariables()
        context["condition"] = condition
        context["diet_type"] = diet_type
        
        result = await self.kernel.run_async(
            self.skills["search_videos"],
            input_vars=context
        )
        
        videos = json.loads(result)
        return videos
    
    async def process(self, search_request):
        # Convertir el JSON a un objeto Python si es necesario
        if isinstance(search_request, str):
            search_request = json.loads(search_request)
        
        # Buscar recetas
        recipes = await self.find_recipes(
            search_request["diet_type"],
            search_request.get("restrictions", [])
        )
        
        # Buscar videos
        videos = await self.find_videos(
            search_request["condition"],
            search_request["diet_type"]
        )
        
        return {
            "recipes": recipes,
            "videos": videos
        }