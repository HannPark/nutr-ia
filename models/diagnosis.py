from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Diagnosis(BaseModel):
    """Modelo para el diagnóstico nutricional"""

    bmi: Optional[float] = Field(None, description="Índice de Masa Corporal")
    bmi_category: str = Field(..., description="Categoría según IMC")
    condition: str = Field(..., description="Condición principal diagnosticada")
    category: Literal[
        "underweight",
        "normal_weight",
        "overweight",
        "obesity_1",
        "obesity_2",
        "obesity_3"
    ] = Field(..., description="Categoría de peso")
    basal_metabolic_rate: float = Field(..., description="Tasa metabólica basal (kcal/día)")
    daily_caloric_needs: float = Field(..., description="Necesidades calóricas diarias")
    potential_deficiencies: List[str] = Field(default_factory=list, description="Deficiencias nutricionales potenciales")
    risk_factors: List[str] = Field(default_factory=list, description="Factores de riesgo identificados")
    description: str = Field(..., description="Explicación del diagnóstico")
    confidence_level: Literal["low", "medium", "high"] = Field(..., description="Nivel de confianza del diagnóstico")

    class Config:
        schema_extra = {
            "example": {
                "bmi": 31.02,
                "bmi_category": "Obesidad Grado I",
                "condition": "Obesidad con hipertensión leve",
                "category": "obesity_1",
                "basal_metabolic_rate": 1850.5,
                "daily_caloric_needs": 2220.6,
                "potential_deficiencies": ["vitamina D", "magnesio"],
                "risk_factors": ["riesgo cardiovascular moderado", "riesgo de diabetes tipo 2"],
                "description": "El paciente presenta obesidad grado I con hipertensión leve. Se recomienda un plan de dieta y ejercicio.",
                "confidence_level": "high"
            }
        }