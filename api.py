# api.py
from fastapi import FastAPI, Request, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
from agents.consultant_agent import ConsultantAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.searcher_agent import SearcherAgent
from models.user_data import UserData

app = FastAPI(title="NUTR-IA API")

# Configurar CORS para permitir peticiones desde tu frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Ajusta al origen de tu aplicación Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar los agentes
consultant = ConsultantAgent()
nutritionist = NutritionistAgent()
searcher = SearcherAgent()

active_connections = {}

@app.post("/api/assessment")
async def assess_patient(
    patient_info: str = Form(...),
    image: UploadFile = File(None)
):
    """Endpoint para iniciar una evaluación de paciente."""
    try:
        # Guardar imagen temporal si existe
        image_path = None
        if image:
            image_path = f"temp/{image.filename}"
            os.makedirs("temp", exist_ok=True)
            with open(image_path, "wb") as f:
                f.write(await image.read())
        
        # 1. Agente Consultor recopila datos
        print("1. Agente Consultor recopilando datos...")
        patient_data = await consultant.process(patient_info, image_path)
        print("tipo de paciente::", type(patient_data))
        # 2. Agente Nutriólogo genera diagnóstico y plan
        print("\n2. Agente Nutriólogo generando diagnóstico y plan...")
        nutritionist_result = await nutritionist.process(patient_data)
        
        # 3. Agente Buscador encuentra recursos
        print("\n3. Agente Buscador encontrando recursos...")
        search_resources = await searcher.process(nutritionist_result["search_request"])
        
        # 4. Compilar respuesta final
        final_result = {
            "patient_data": patient_data,
            "diagnosis": nutritionist_result["diagnosis"],
            "diet_plan": nutritionist_result["diet_plan"],
            "exercise_routine": nutritionist_result["exercise_routine"],
            "recipes": search_resources["recipes"],
            "videos": search_resources["videos"]
        }
        
        # Eliminar imagen temporal si existe
        print("Eliminando imagen temporal...")
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            
        return final_result
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws/assessment")
async def websocket_endpoint(websocket: WebSocket):
    """Punto de conexión WebSocket para seguimiento en tiempo real del proceso."""
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        request = json.loads(data)
        
        # Notificar inicio del proceso
        await websocket.send_json({"status": "Iniciando proceso de evaluación"})
        
        # 1. Agente Consultor recopila datos
        await websocket.send_json({"status": "Recopilando datos del paciente"})
        patient_data = await consultant.process(request["patient_info"])
        await websocket.send_json({"status": "Datos del paciente recopilados", "data": patient_data})
        
        # 2. Agente Nutriólogo genera diagnóstico y plan
        await websocket.send_json({"status": "Generando diagnóstico y plan nutricional"})
        nutritionist_result = await nutritionist.process(patient_data)
        await websocket.send_json({"status": "Diagnóstico y plan generados", "data": nutritionist_result})
        
        # 3. Agente Buscador encuentra recursos
        await websocket.send_json({"status": "Buscando recursos adicionales"})
        search_resources = await searcher.process(nutritionist_result["search_request"])
        
        # 4. Compilar respuesta final
        final_result = {
            "patient_data": patient_data,
            "diagnosis": nutritionist_result["diagnosis"],
            "diet_plan": nutritionist_result["diet_plan"],
            "exercise_routine": nutritionist_result["exercise_routine"],
            "recipes": search_resources["recipes"],
            "videos": search_resources["videos"]
        }
        
        await websocket.send_json({"status": "Proceso completado", "data": final_result})
        
    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        await websocket.close()

@app.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    # Inicializar el agente y los datos del usuario
    user_data = UserData()
    try:
        await consultant.process_chat(websocket, user_data)
    except WebSocketDisconnect:
        if client_id in active_connections:
            del active_connections[client_id]
    except Exception as e:
        # Enviar mensaje de error
        await websocket.send_json({
            "sender": "system",
            "message": f"Error: {str(e)}"
        })
        # Cerrar conexión
        if client_id in active_connections:
            del active_connections[client_id]

@app.post("/api/assessment-with-data")
async def assess_patient_with_data(
    request: Request
):
    """Endpoint para iniciar una evaluación de paciente."""
    try:
        patient_info = await request.json()
        
        print("\n1. patient_info::", patient_info)
        print("tipo de paciente::", type(patient_info))
        # 2. Agente Nutriólogo genera diagnóstico y plan
        print("\n2. Agente Nutriólogo generando diagnóstico y plan...")
        nutritionist_result = await nutritionist.process(patient_info)
        
        # 3. Agente Buscador encuentra recursos
        print("\n3. Agente Buscador encontrando recursos...")
        search_resources = await searcher.process(nutritionist_result["search_request"])
        
        # 4. Compilar respuesta final
        final_result = {
            "patient_data": patient_info,
            "diagnosis": nutritionist_result["diagnosis"],
            "diet_plan": nutritionist_result["diet_plan"],
            "exercise_routine": nutritionist_result["exercise_routine"],
            "recipes": search_resources["recipes"],
            "videos": search_resources["videos"]
        }
        return final_result
    except Exception as e:
        return {"error": str(e)}

# Punto de entrada para ejecutar la API
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)