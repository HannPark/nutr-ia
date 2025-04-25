from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json

class GatherDataSkill:
    @sk_function(
        description="Recopila datos nutricionales del paciente a través de preguntas",
        name="gather_data"
    )
    @sk_function_context_parameter(
        name="input",
        description="Información inicial proporcionada por el paciente"
    )
    async def gather_data(self, context: SKContext) -> str:
        """
        Recopila información nutricional completa del paciente basada en su input inicial.
        Realiza preguntas adicionales si es necesario y estructura los datos.
        """
        patient_input = context["input"]
        
        # Sistema: prompt para que el modelo actúe como un consultor nutricional
        prompt = f"""
        Eres un especialista en nutrición altamente calificado que está entrevistando a un paciente.
        Analiza la siguiente información proporcionada por el paciente:
        
        "{patient_input}"
        
        Extrae todos los datos nutricionales y físicos relevantes como:
        - Edad
        - Género
        - Altura
        - Peso actual
        - Objetivo de peso
        - Nivel de actividad física
        - Alergias o intolerancias alimentarias
        - Preferencias alimentarias
        - Condiciones médicas relevantes
        - Historial de dietas previas
        
        Si la información no está completa, indica qué datos faltan que serían importantes preguntar.
        
        Organiza la información en un objeto JSON con los siguientes campos:
        {
            "age": int o null,
            "gender": string o null,
            "height_cm": float o null,
            "weight_kg": float o null,
            "target_weight_kg": float o null,
            "activity_level": "sedentary" | "lightly_active" | "moderately_active" | "very_active" | "extremely_active" o null,
            "allergies": [lista de strings] o [],
            "dietary_preferences": [lista de strings] o [],
            "dietary_restrictions": [lista de strings] o [],
            "medical_conditions": [lista de strings] o [],
            "previous_diets": [lista de strings] o [],
            "missing_info": [lista de strings con datos importantes que faltan] o []
        }
        
        Devuelve SOLO el objeto JSON, sin texto adicional.
        """

        # Obtener respuesta del modelo de lenguaje
        response = await context.variables.kernel.memory.semantic_question(prompt)
        
        # Asegurar que la respuesta sea un JSON válido
        try:
            # Limpiar posibles marcadores de código que podrían haberse incluido
            json_str = response.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            json_str = json_str.strip()
            result = json.loads(json_str)
            return json.dumps(result, indent=2)
        except json.JSONDecodeError:
            # Si hay error, devolver un JSON con error
            return json.dumps({
                "error": "No se pudo procesar la información del paciente",
                "raw_input": patient_input
            })