import json
from semantic_kernel import Kernel
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter

from utils.openai_utils import OpenAIUtils

class ExtractUserInfoSkill:
    @sk_function(
        description="Extrae información del usuario a partir de su respuesta",
        name="extract_user_info"
    )
    @sk_function_context_parameter(
        name="input",
        description="Array entrante con informacion del paciente"
    )
    @sk_function_context_parameter(
        name="kernel",
        description="Kernel de Semantic Kernel"
    )
    @sk_function_context_parameter(
        name="respuesta_paciente",
        description="Respuesta del paciente"
    )
    @sk_function_context_parameter(
        name="campo_respuesta",
        description="Campo a agregar al array"
    )
    async def extract_user_info(self, context: SKContext) -> str:
        input = context["input"]
        print("Input::", input)
        user_message = context["respuesta_paciente"]
        print("User message::", user_message)
        campo_respuesta = context["campo_respuesta"]
        print("Campo respuesta::", campo_respuesta)
        # Obtener el kernel del contexto
        kernel: Kernel = context["kernel"]
        # Sistema: prompt para que el modelo actúe como un consultor nutricional
        prompt = f"""
        Eres un especialista en nutrición altamente calificado que está entrevistando a un paciente.
        El siguiente array que es el que vamos a modificar con la respuesta del paciente:

        "{input}"

        El paciente quiere agregar la siguiente información: "{user_message}",
        en el campo "{campo_respuesta}" del array, agrega la información relevante que el paciente ha proporcionado,
        Asegúrate de que la información esté bien estructurada y sea coherente con el resto del array.

        Elimina el campo "{campo_respuesta}" de la lista "missing_info" si existe, ya que el paciente ha proporcionado la información necesaria.

        Organiza la información en un objeto JSON con la misma estructura del array inicial, sin modificar los demás campos, 
        ni el orden de los demas campos de la key "missing_info", si ya todos los demas campos del array están completos o tienen alguna información, deja el campo "missing_info" vacío.:
        {{
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
        }}

        Devuelve SOLO el objeto JSON, sin texto adicional.
        """
        # Obtener respuesta del modelo de lenguaje
        # response = await context.variables.kernel.memory.semantic_question(prompt)
        response:str = await OpenAIUtils.ai_semantic_question(kernel, prompt)
        print("Response::", response)

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
                "raw_input": input
            })