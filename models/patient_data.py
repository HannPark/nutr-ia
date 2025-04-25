from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class PatientData(BaseModel):
    """Modelo para los datos del paciente"""

    age: Optional[int] = Field(None, description="Edad del paciente en años")
    gender: Optional[str] = Field(None, description="Género del paciente")
    height_cm: Optional[float] = Field(None, description="Altura en centímetros")
    weight_kg: Optional[float] = Field(None, description="Peso actual en kilogramos")
    target_weight_kg: Optional[float] = Field(None, description="Peso objetivo en kilogramos")
    activity_level: Optional[Literal[
        "sedentary",
        "lightly_active",
        "moderately_active",
        "very_active",
        "extremely_active"
    ]] = Field(None, description="Nivel de actividad física")
    allergies: List[str] = Field(default_factory=list, description="Lista de alergias alimentarias")
    dietary_preferences: List[str] = Field(default_factory=list, description="Preferencias alimentarias")
    dietary_restrictions: List[str] = Field(default_factory=list, description="Restricciones dietéticas")
    medical_conditions: List[str] = Field(default_factory=list, description="Condiciones médicas relevantes")
    previous_diets: List[str] = Field(default_factory=list, description="Dietas previas")
    missing_info: List[str] = Field(default_factory=list, description="Información faltante importante")
    
    # Datos adicionales del análisis de imagen (si está disponible)
    body_type: Optional[str] = Field(None, description="Tipo de cuerpo (ectomorfo, mesomorfo, endomorfo)")
    fat_distribution: Optional[str] = Field(None, description="Distribución de grasa corporal")
    estimated_body_fat: Optional[str] = Field(None, description="Porcentaje estimado de grasa corporal")
    
    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "gender": "masculino",
                "height_cm": 175,
                "weight_kg": 95,
                "target_weight_kg": 80,
                "activity_level": "sedentary",
                "allergies": ["lactosa"],
                "dietary_preferences": ["pollo", "pescado", "vegetales verdes"],
                "dietary_restrictions": ["mariscos"],
                "medical_conditions": ["hipertensión leve"],
                "previous_diets": ["keto por 2 meses"],
                "missing_info": [],
                "body_type": "mesomorfo",
                "fat_distribution": "predominantemente abdominal",
                "estimated_body_fat": "25-30%"
            }
        }