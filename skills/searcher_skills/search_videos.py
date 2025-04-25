from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json

class SearchVideosSkill:
    @sk_function(
        description="Busca videos informativos relacionados con nutrición y condiciones específicas",
        name="search_videos"
    )
    @sk_function_context_parameter(
        name="condition",
        description="Condición o diagnóstico del paciente"
    )
    @sk_function_context_parameter(
        name="diet_type",
        description="Tipo de dieta recomendada"
    )
    async def search_videos(self, context: SKContext) -> str:
        """
        Busca y recomienda videos informativos relacionados con la condición del paciente y el tipo de dieta.
        """
        condition = context["condition"]
        diet_type = context["diet_type"]
        
        # Sistema: prompt para buscar videos
        prompt = f"""
        Eres un especialista en contenido educativo sobre nutrición y salud.
        
        Necesito recomendaciones de videos informativos relacionados con:
        - Condición: {condition}
        - Tipo de dieta: {diet_type}
        
        Proporciona 5 recomendaciones de videos que:
        1. Sean informativos y basados en ciencia
        2. Sean útiles para pacientes con esta condición
        3. Expliquen aspectos relevantes de la dieta recomendada
        4. Proporcionen consejos prácticos aplicables
        5. Sean de fuentes confiables (profesionales médicos, dietistas registrados, instituciones reconocidas)
        
        Para cada video, incluye:
        - Título descriptivo
        - Descripción del contenido
        - Duración aproximada
        - Autor/Canal (hipotético pero realista)
        - Puntos clave que cubre
        
        Organiza las recomendaciones en un array JSON con esta estructura:
        [
            {
                "title": string (título del video),
                "description": string (descripción del contenido),
                "duration_minutes": int (duración aproximada),
                "author": string (autor o canal),
                "key_points": [lista de puntos clave que cubre],
                "recommended_for": [tipos de pacientes que se beneficiarían],
                "expertise_level": "beginner" | "intermediate" | "advanced",
                "tags": [lista de etiquetas relevantes]
            }
        ]
        
        Devuelve SOLO el array JSON, sin texto adicional.
        """
        
        # Obtener respuesta del modelo de lenguaje
        response = await context.variables.kernel.memory.semantic_question(prompt)
        
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
                "error": "No se pudieron generar recomendaciones de videos válidas",
                "raw_response": response
            })