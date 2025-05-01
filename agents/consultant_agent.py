import json
from fastapi import WebSocket
import semantic_kernel as sk
from config.openai_config import OpenAIConfig
from models.user_data import UserData
from skills.consultant.extract_user_info import ExtractUserInfoSkill
from skills.consultant.get_next_question import GetNextQuestionSkill
from .base_agent import BaseAgent
from skills.consultant.analyze_image import AnalyzeImageSkill
from skills.consultant.gather_data import GatherDataSkill

class ConsultantAgent(BaseAgent):
    def __init__(self):
        self.native_skills = {
            "analyze_image": AnalyzeImageSkill(),
            "gather_data":GatherDataSkill(),
            "get_next_question": GetNextQuestionSkill(),
            "extract_user_info": ExtractUserInfoSkill(),
        }
        super().__init__("consultant", OpenAIConfig.CONSULTANT_MODEL)
        self.skills = self.load_skills("skills/",native=self.native_skills)
    
    async def get_next_question(self, array):
        # Implementar lógica para recopilar datos del paciente
        context = sk.ContextVariables()
        context["input"] = array
        context["kernel"] = self.kernel

        # Usar la habilidad para hacer preguntas al paciente
        skill_response = await self.kernel.run_async(
            self.skills["get_next_question"],
            input_vars=context
        )

        return skill_response.result

    async def update_patient_info(self, patient_info, respuesta_paciente, campo_respuesta):
        # Implementar lógica para recopilar datos del paciente
        context = sk.ContextVariables()
        context["input"] = patient_info,
        context["respuesta_paciente"] = respuesta_paciente
        context["campo_respuesta"] = campo_respuesta
        context["kernel"] = self.kernel

        # Usar la habilidad para hacer preguntas al paciente
        skill_response = await self.kernel.run_async(
            self.skills["extract_user_info"],
            input_vars=context
        )

        patient_data = json.loads(skill_response.result)
        return patient_data
    
    async def collect_patient_data(self, patient_input):
        # Implementar lógica para recopilar datos del paciente
        context = sk.ContextVariables()
        context["input"] = patient_input
        context["kernel"] = self.kernel

        # Usar la habilidad para hacer preguntas al paciente
        skill_response = await self.kernel.run_async(
            self.skills["gather_data"],
            input_vars=context
        )
        
        # Procesar el resultado y crear un JSON estructurado
        patient_data = json.loads(skill_response.result)
        return patient_data
    
    async def analyze_screenshot(self, image_path):
        # Implementar análisis de screenshot
        # Esto podría usar OpenAI Vision API para analizar la composición corporal
        context = sk.ContextVariables()
        context["image_path"] = image_path
        context["kernel"] = self.kernel

        skill_response = await self.kernel.run_async(
            self.skills["analyze_image"],
            input_vars=context
        )
        
        image_data = json.loads(skill_response.result)
        return image_data
    
    async def process(self, patient_info, image_path=None):
        # Recopilar datos básicos del paciente
        patient_data = await self.collect_patient_data(patient_info)
        
        # Si hay imagen, analizarla
        if image_path:
            image_analysis = await self.analyze_screenshot(image_path)
            patient_data.update(image_analysis)
        
        # Generar el JSON final para el Nutriólogo
        return patient_data
    
    async def process_chat(self, websocket: WebSocket, user_data: UserData) -> None:
        # Enviar mensaje de bienvenida
        welcome_message = {
            "sender": "system",
            "message": "¡Bienvenido al asistente nutricional! Voy a hacerte algunas preguntas para completar tu evaluación."
        }
        await websocket.send_json(welcome_message)
        # Enviar la primera pregunta
        array_patient_info = json.dumps(user_data.data)
        first_question = await self.get_next_question(array_patient_info)
        await websocket.send_json({
            "sender": "bot",
            "message": first_question
        })
        
        # Bucle principal de chat
        while True:
            # Recibir mensaje del usuario
            user_message_data = await websocket.receive_json()
            user_message = user_message_data.get("message", "")
            # Enviar acuse de recibo
            await websocket.send_json({
                "sender": "system",
                "message": "Procesando tu respuesta..."
            })
            
            # Extraer información de la respuesta del usuario
            patient_info = json.dumps(user_data.data)
            campo_respuesta = user_data.data["missing_info"][0] if user_data.data["missing_info"] else None
            extraction_result = await self.update_patient_info(patient_info,user_message,campo_respuesta)
            print("Extraction Result::", extraction_result)
            if extraction_result:
                user_data.data = extraction_result

                # Enviar confirmación al usuario
                confirm_message = f"he registrado tu {campo_respuesta}"
                await websocket.send_json({
                    "sender": "bot",
                    "message": confirm_message
                })
                
                # Si todos los datos están completos, terminar
                if user_data.is_complete():
                    final_message = "¡Excelente! He recopilado toda la información necesaria para tu evaluación nutricional."
                    await websocket.send_json({
                        "sender": "bot",
                        "message": final_message
                    })
                    
                    # Enviar los datos completos
                    await websocket.send_json({
                        "sender": "system",
                        "message": "Información completa",
                        "data": user_data.data
                    })
                    break
                
                # Obtener la siguiente pregunta
                next_question = await self.get_next_question(json.dumps(user_data.data))
                
                await websocket.send_json({
                    "sender": "bot",
                    "message": next_question
                })
            else:
                # Si no se pudo extraer información, pedir aclaración
                await websocket.send_json({
                    "sender": "bot",
                    "message": "Lo siento, no pude entender tu respuesta. Por favor, intenta de nuevo."
                })