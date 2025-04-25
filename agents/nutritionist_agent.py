import json
import semantic_kernel as sk
from config.openai_config import OpenAIConfig
from .base_agent import BaseAgent

class NutritionistAgent(BaseAgent):
    def __init__(self):
        super().__init__("nutritionist", OpenAIConfig.NUTRITIONIST_MODEL)
        self.skills = self.load_skills("skills/nutritionist_skills")
    
    async def diagnose_condition(self, patient_data):
        # Diagnosticar condición basado en datos del paciente
        context = sk.ContextVariables()
        context["patient_data"] = json.dumps(patient_data)
        
        result = await self.kernel.run_async(
            self.skills["diagnose"],
            input_vars=context
        )
        
        diagnosis = json.loads(result)
        return diagnosis
    
    async def create_diet_plan(self, patient_data, diagnosis):
        # Crear plan de dieta basado en diagnóstico
        context = sk.ContextVariables()
        context["patient_data"] = json.dumps(patient_data)
        context["diagnosis"] = json.dumps(diagnosis)
        
        result = await self.kernel.run_async(
            self.skills["create_diet"],
            input_vars=context
        )
        
        diet_plan = json.loads(result)
        return diet_plan
    
    async def generate_exercise_routine(self, patient_data, diagnosis):
        # Generar rutina de ejercicios
        context = sk.ContextVariables()
        context["patient_data"] = json.dumps(patient_data)
        context["diagnosis"] = json.dumps(diagnosis)
        
        result = await self.kernel.run_async(
            self.skills["create_exercise_routine"],
            input_vars=context
        )
        
        exercise_routine = json.loads(result)
        return exercise_routine
    
    async def process(self, patient_data_json):
        # Convertir el JSON a un objeto Python
        patient_data = json.loads(patient_data_json) if isinstance(patient_data_json, str) else patient_data_json
        
        # Realizar diagnóstico
        diagnosis = await self.diagnose_condition(patient_data)
        
        # Crear plan de dieta
        diet_plan = await self.create_diet_plan(patient_data, diagnosis)
        
        # Generar rutina de ejercicios
        exercise_routine = await self.generate_exercise_routine(patient_data, diagnosis)
        
        # Solicitar información al agente buscador
        search_request = {
            "diet_type": diet_plan["diet_type"],
            "condition": diagnosis["condition"],
            "restrictions": patient_data.get("dietary_restrictions", [])
        }
        
        return {
            "diagnosis": diagnosis,
            "diet_plan": diet_plan,
            "exercise_routine": exercise_routine,
            "search_request": search_request
        }