from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import json
import base64

class AnalyzeImageSkill:
    @sk_function(
        description="Analiza la imagen del paciente para estimar composición corporal",
        name="analyze_image"
    )
    @sk_function_context_parameter(
        name="image_path",
        description="Ruta a la imagen del paciente"
    )
    async def analyze_image(self, context: SKContext) -> str:
        """
        Analiza la imagen del paciente para estimar composición corporal y otros indicadores visuales.
        Utiliza OpenAI Vision para el análisis.
        """
        image_path = context["image_path"]
        
        # Codificar la imagen en base64
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            return json.dumps({
                "error": f"No se pudo procesar la imagen: {str(e)}"
            })
        
        # Sistema: prompt para análisis de imagen
        prompt_messages = [
            {
                "role": "system",
                "content": """Eres un especialista en composición corporal y antropometría. 
                Tu trabajo es analizar imágenes de pacientes y estimar indicadores como:
                - Tipo de cuerpo (ectomorfo, mesomorfo, endomorfo)
                - Distribución aproximada de grasa corporal
                - Signos visibles relacionados con nutrición
                
                Proporciona estimaciones conservadoras y menciona el nivel de confianza de tu análisis."""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analiza esta imagen y proporciona estimaciones sobre composición corporal y tipo de cuerpo."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ]
        
        # Esta función necesitaría implementar una llamada al API de visión de OpenAI
        # El siguiente código es un placeholder para la integración real
        
        # En una implementación real, se usaría:
        # response = await openai.ChatCompletion.create(
        #    model="gpt-4-vision-preview",
        #    messages=prompt_messages,
        #    max_tokens=500
        # )
        # analysis_text = response.choices[0].message.content
        
        # Por ahora, usaremos un ejemplo genérico
        analysis_result = {
            "body_type": "mesomorfo",
            "fat_distribution": "predominantemente abdominal",
            "estimated_body_fat": "25-30%",
            "visible_indicators": [
                "retención de líquidos moderada",
                "tono muscular moderado"
            ],
            "confidence_level": "medio",
            "recommendations": [
                "enfoque en reducción de grasa abdominal",
                "entrenamiento de fuerza para mantener masa muscular"
            ]
        }
        
        return json.dumps(analysis_result, indent=2)