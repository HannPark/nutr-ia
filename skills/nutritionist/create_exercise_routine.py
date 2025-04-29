from semantic_kernel import Kernel
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json

from utils.openai_utils import OpenAIUtils

class CreateExerciseRoutineSkill:
    @sk_function(
        description="Crea una rutina de ejercicios personalizada",
        name="create_exercise_routine"
    )
    @sk_function_context_parameter(
        name="patient_data",
        description="Datos del paciente en formato JSON"
    )
    @sk_function_context_parameter(
        name="diagnosis",
        description="Diagnóstico nutricional en formato JSON"
    )
    async def create_exercise_routine(self, context: SKContext) -> str:
        """
        Crea una rutina de ejercicios personalizada basada en los datos del paciente y su diagnóstico.
        """
        try:
            patient_data = json.loads(context["patient_data"])
            diagnosis = json.loads(context["diagnosis"])
        except json.JSONDecodeError:
            return json.dumps({"error": "Datos de entrada en formato inválido"})

        kernel: Kernel = context["kernel"]

        # Sistema: prompt para crear rutina de ejercicios
        prompt = f"""
        Eres un especialista en medicina deportiva y ejercicio físico.
        Con base en los siguientes datos del paciente y su diagnóstico nutricional:
        
        DATOS DEL PACIENTE:
        {json.dumps(patient_data, indent=2)}
        
        DIAGNÓSTICO:
        {json.dumps(diagnosis, indent=2)}
        
        Crea una rutina de ejercicios que:
        
        1. Sea adecuada para la condición física actual del paciente
        2. Considere cualquier limitación física o condiciones médicas
        3. Sea progresiva y escalable según mejore su condición
        4. Complemente el plan nutricional para lograr sus objetivos
        5. Sea realista y sostenible para incorporar en su vida diaria
        6. Se pueda realizar principalmente en casa con equipo mínimo
        
        Organiza la rutina en un objeto JSON con la siguiente estructura:
        {{
            "fitness_level": string (nivel recomendado: "principiante", "intermedio", "avanzado"),
            "sessions_per_week": int (número recomendado de sesiones),
            "description": string (descripción general de la rutina),
            "exercises": [
                {{
                    "name": string (nombre del ejercicio),
                    "type": string (tipo: "cardiovascular", "fuerza", "flexibilidad", "equilibrio"),
                    "description": string (descripción breve),
                    "duration": string (duración o repeticiones),
                    "frequency": string (frecuencia semanal),
                    "intensity": string (intensidad recomendada),
                    "progression": string (cómo progresar)
                }}
            ],
            "weekly_schedule": {{
                "monday": [lista de ejercicios recomendados],
                "tuesday": [],
                ...
                "sunday": []
            }},
            "precautions": [lista de precauciones a tomar],
            "goals": [lista de objetivos de la rutina]
        }}
        
        Incluye máximo 5-7 ejercicios diferentes que sean complementarios entre sí.
        
        Devuelve SOLO el objeto JSON, sin texto adicional.
        """
        
        # Obtener respuesta del modelo de lenguaje
        response:str = await OpenAIUtils.ai_semantic_question(kernel, prompt)
        
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
                "error": "No se pudo generar una rutina de ejercicios válida",
                "raw_response": response
            })