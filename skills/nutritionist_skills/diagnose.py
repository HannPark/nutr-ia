from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json

class DiagnoseSkill:
    @sk_function(
        description="Diagnostica la condición nutricional del paciente",
        name="diagnose"
    )
    @sk_function_context_parameter(
        name="patient_data",
        description="Datos del paciente en formato JSON"
    )
    async def diagnose(self, context: SKContext) -> str:
        """
        Analiza los datos del paciente y diagnostica su condición nutricional.
        Determina su IMC, categoría de peso y otras métricas relevantes.
        """
        try:
            patient_data = json.loads(context["patient_data"])
        except json.JSONDecodeError:
            return json.dumps({"error": "Datos del paciente en formato inválido"})
        
        # Sistema: prompt para diagnóstico
        prompt = f"""
        Eres un especialista en nutrición clínica. Con base en los siguientes datos del paciente:
        
        {json.dumps(patient_data, indent=2)}
        
        Realiza un diagnóstico nutricional completo que incluya:
        
        1. Cálculo del IMC (si se dispone de altura y peso)
        2. Clasificación según IMC (bajo peso, normopeso, sobrepeso, obesidad grado I, II o III)
        3. Estimación del metabolismo basal usando la fórmula de Mifflin-St Jeor
        4. Requerimiento calórico diario estimado basado en nivel de actividad
        5. Evaluación de potenciales deficiencias nutricionales basadas en preferencias y restricciones
        6. Factores de riesgo identificados
        
        Organiza tu diagnóstico en un objeto JSON con los siguientes campos:
        {
            "bmi": float o null,
            "bmi_category": string,
            "condition": string (condición principal),
            "category": "underweight" | "normal_weight" | "overweight" | "obesity_1" | "obesity_2" | "obesity_3",
            "basal_metabolic_rate": float (kcal/día),
            "daily_caloric_needs": float (kcal/día),
            "potential_deficiencies": [lista de strings],
            "risk_factors": [lista de strings],
            "description": string (explicación del diagnóstico),
            "confidence_level": "low" | "medium" | "high"
        }
        
        Si faltan datos críticos para algún cálculo, asigna null a ese valor y menciona los datos faltantes en la descripción.
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
                "error": "No se pudo generar un diagnóstico válido",
                "raw_response": response
            })