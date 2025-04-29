from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json

class CreateDietSkill:
    @sk_function(
        description="Crea un plan de dieta personalizado",
        name="create_diet"
    )
    @sk_function_context_parameter(
        name="patient_data",
        description="Datos del paciente en formato JSON"
    )
    @sk_function_context_parameter(
        name="diagnosis",
        description="Diagnóstico nutricional en formato JSON"
    )
    async def create_diet(self, context: SKContext) -> str:
        """
        Crea un plan de dieta personalizado basado en los datos del paciente y su diagnóstico.
        """
        try:
            patient_data = json.loads(context["patient_data"])
            diagnosis = json.loads(context["diagnosis"])
        except json.JSONDecodeError:
            return json.dumps({"error": "Datos de entrada en formato inválido"})
        
        # Sistema: prompt para crear dieta
        prompt = f"""
        Eres un nutriólogo especializado en crear planes de alimentación personalizados.
        Con base en los siguientes datos del paciente y su diagnóstico nutricional:
        
        DATOS DEL PACIENTE:
        {json.dumps(patient_data, indent=2)}
        
        DIAGNÓSTICO:
        {json.dumps(diagnosis, indent=2)}
        
        Crea un plan de alimentación mensual que:
        
        1. Sea adecuado para la condición del paciente y su diagnóstico
        2. Respete sus preferencias alimentarias y restricciones dietéticas
        3. Tenga como objetivo principal: {patient_data.get("target_weight_kg", "mejorar la salud general") if patient_data.get("target_weight_kg") else "mejorar la salud general"}
        4. Incluya una distribución adecuada de macronutrientes
        5. Considere cualquier deficiencia nutricional potencial identificada
        6. Sea realista y sostenible a largo plazo
        
        Organiza el plan en un objeto JSON con la siguiente estructura:
        {
            "diet_type": string (tipo de dieta recomendada, ej: "hipocalórica equilibrada"),
            "daily_calories": float (calorías diarias recomendadas),
            "macronutrients": {
                "protein_percentage": float,
                "carbs_percentage": float,
                "fat_percentage": float
            },
            "meals": [
                {
                    "name": string (nombre de la comida, ej: "Desayuno"),
                    "time": string (horario recomendado),
                    "calories": float (proporción de calorías diarias),
                    "items": [lista de alimentos/platos recomendados]
                }
            ],
            "food_groups_to_prioritize": [lista de strings],
            "food_groups_to_limit": [lista de strings],
            "recommendations": string (recomendaciones generales),
            "supplements": [lista de suplementos recomendados, si aplica]
        }
        
        Incluye 5 comidas diarias (desayuno, media mañana, almuerzo, merienda, cena).
        Para cada comida, sugiere 3-5 opciones de alimentos o platos adecuados.
        
        Devuelve SOLO el objeto JSON, sin texto adicional.
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
                "error": "No se pudo generar un plan de dieta válido",
                "raw_response": response
            })