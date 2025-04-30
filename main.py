import asyncio
import json
from agents.consultant_agent import ConsultantAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.searcher_agent import SearcherAgent

async def main():
    # Crear instancias de los agentes
    consultant = ConsultantAgent()
    nutritionist = NutritionistAgent()
    searcher = SearcherAgent()
    
    # Ejemplo de flujo de trabajo
    patient_input = "Necesito una dieta para reducir mi peso. Tengo 35 años, mido 1.75m y peso 95kg. Soy sedentario y no me gustan los mariscos."
    
    # 1. El agente consultor recopila información del paciente
    print("1. Agente Consultor recopilando datos...")
    patient_data = await consultant.process(patient_input)
    print(f"Datos del paciente: {json.dumps(patient_data, indent=2)}")
    
    # 2. El agente nutriólogo analiza los datos y genera un diagnóstico y plan
    print("\n2. Agente Nutriólogo generando diagnóstico y plan...")
    nutritionist_result = await nutritionist.process(patient_data)
    print(f"Diagnóstico: {json.dumps(nutritionist_result['diagnosis'], indent=2)}")
    print(f"Plan de dieta: {json.dumps(nutritionist_result['diet_plan'], indent=2)}")
    
    # 3. El agente buscador encuentra recetas y videos relevantes
    print("\n3. Agente Buscador encontrando recursos...")
    search_resources = await searcher.process(nutritionist_result["search_request"])
    print(f"Recetas encontradas: {json.dumps(search_resources['recipes'], indent=2)}")
    print(f"Videos encontrados: {json.dumps(search_resources['videos'], indent=2)}")
    
    # 4. Compilar respuesta final
    final_result = {
        "patient_data": patient_data,
        "diagnosis": nutritionist_result["diagnosis"],
        "diet_plan": nutritionist_result["diet_plan"],
        "exercise_routine": nutritionist_result["exercise_routine"],
        "recipes": search_resources["recipes"],
        "videos": search_resources["videos"]
    }
    
    print("\n4. Resultado final compilado para el paciente")
    print(json.dumps(final_result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())