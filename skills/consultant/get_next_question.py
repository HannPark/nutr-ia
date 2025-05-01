import json
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext

class GetNextQuestionSkill:
    @sk_function(
        description="Genera la siguiente pregunta basada en la información faltante",
        name="get_next_question"
    )
    @sk_function_context_parameter(
        name="input",
        description="Información inicial proporcionada por el paciente"
    )
    def get_next_question(self, context: SKContext) -> str:
        """Genera la siguiente pregunta basada en la información que falta"""
        user_data = json.loads(context["input"])
        if not user_data["missing_info"]:
            return "¡Gracias! He recopilado toda la información necesaria para tu evaluación nutricional."
        
        next_info = user_data["missing_info"][0]
        questions = {
            "age": "¿Cuál es tu edad?",
            "gender": "¿Cuál es tu género? (masculino/femenino/otro)",
            "height_cm": "¿Cuál es tu altura en centímetros?",
            "weight_kg": "¿Cuál es tu peso actual en kilogramos?",
            "target_weight_kg": "¿Cuál es tu peso objetivo en kilogramos?",
            "activity_level": "¿Cuál es tu nivel de actividad física? (sedentario/ligeramente activo/moderadamente activo/muy activo/extremadamente activo)",
            "allergies": "¿Tienes alguna alergia alimentaria? Por favor, enuméralas separadas por comas, o escribe 'ninguna'.",
            "dietary_preferences": "¿Tienes preferencias dietéticas? (vegetariano, vegano, etc.) Enuméralas separadas por comas, o escribe 'ninguna'.",
            "dietary_restrictions": "¿Tienes restricciones dietéticas? Enuméralas separadas por comas, o escribe 'ninguna'.",
            "medical_conditions": "¿Tienes condiciones médicas que afecten tu dieta? Enuméralas separadas por comas, o escribe 'ninguna'.",
            "previous_diets": "¿Has seguido dietas anteriormente? Enuméralas separadas por comas, o escribe 'ninguna'."
        }
        
        return questions.get(next_info, f"Por favor, proporcióneme su {next_info}:")