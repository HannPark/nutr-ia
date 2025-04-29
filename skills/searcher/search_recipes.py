from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json

from utils.openai_utils import OpenAIUtils

class SearchRecipesSkill:
    @sk_function(
        description="Busca recetas adecuadas para un tipo de dieta específico",
        name="search_recipes"
    )
    @sk_function_context_parameter(
        name="diet_type",
        description="Tipo de dieta recomendada"
    )
    @sk_function_context_parameter(
        name="restrictions",
        description="Restricciones dietéticas en formato JSON array"
    )
    async def search_recipes(self, context: SKContext) -> str:
        """
        Busca y recomienda recetas basadas en el tipo de dieta y restricciones.
        """
        diet_type = context["diet_type"]
        kernel = context["kernel"]

        try:
            restrictions = json.loads(context["restrictions"])
        except json.JSONDecodeError:
            restrictions = []
        
        # Sistema: prompt para buscar recetas
        prompt = f"""
        Eres un especialista culinario con amplio conocimiento de nutrición.
        Necesito recetas adecuadas para el siguiente tipo de dieta: "{diet_type}"
        
        Restricciones dietéticas a considerar: {restrictions if restrictions else "Ninguna específica"}
        
        Proporciona 5 recetas que:
        1. Se alineen perfectamente con este tipo de dieta
        2. Respeten todas las restricciones mencionadas
        3. Sean nutritivas y balanceadas
        4. Sean relativamente sencillas de preparar
        5. Utilicen ingredientes comunes y accesibles
        
        Para cada receta incluye:
        - Nombre descriptivo
        - Breve descripción
        - Lista de ingredientes principales (5-8 ingredientes)
        - Macronutrientes aproximados (proteínas, carbohidratos, grasas)
        - Calorías aproximadas por porción
        - Tiempo de preparación
        - Nivel de dificultad
        
        Organiza las recetas en un array JSON con esta estructura:
        [
            {{
                "name": string (nombre de la receta),
                "description": string (descripción breve),
                "main_ingredients": [lista de ingredientes principales],
                "macros": {{
                    "protein": float (gramos),
                    "carbs": float (gramos),
                    "fat": float (gramos)
                }},
                "calories_per_serving": float,
                "prep_time_minutes": int,
                "difficulty": "easy" | "medium" | "hard",
                "meal_type": "breakfast" | "lunch" | "dinner" | "snack",
                "tags": [lista de etiquetas relevantes]
            }}
        ]
        
        Devuelve SOLO el array JSON, sin texto adicional.
        """
        
        # Obtener respuesta del modelo de lenguaje
        response:str = OpenAIUtils.ai_semantic_question(kernel, prompt)
        
        # Procesar respuesta
        try:
            # Limpiar posibles marcadores de código
            json_str = response.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            json_str = json_str.strip()
            result = json.loads(json_str)
            return json.dumps(result, indent=2)
        except json.JSONDecodeError:
            return json.dumps({
                "error": "No se pudieron generar recetas válidas",
                "raw_response": response
            })
