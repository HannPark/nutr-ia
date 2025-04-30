import json
import semantic_kernel as sk
from config.openai_config import OpenAIConfig
from .base_agent import BaseAgent
from skills.consultant.analyze_image import AnalyzeImageSkill
from skills.consultant.gather_data import GatherDataSkill

class ConsultantAgent(BaseAgent):
    def __init__(self):
        self.native_skills = {
            "analyze_image": AnalyzeImageSkill(),
            "gather_data":GatherDataSkill()
        }
        super().__init__("consultant", OpenAIConfig.CONSULTANT_MODEL)
        self.skills = self.load_skills("skills/",native=self.native_skills)
    
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