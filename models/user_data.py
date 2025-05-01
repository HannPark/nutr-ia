from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class UserData:
    def __init__(self):
        self.data = {
            "age": None,
            "gender": None,
            "height_cm": None,
            "weight_kg": None,
            "target_weight_kg": None,
            "activity_level": None,
            "allergies": [],
            "dietary_preferences": [],
            "dietary_restrictions": [],
            "medical_conditions": [],
            "previous_diets": [],
            "missing_info": [
                "age", "gender", "height_cm", "weight_kg", 
                "target_weight_kg", "activity_level",
                "allergies", "dietary_preferences",
                "dietary_restrictions", "medical_conditions",
                "previous_diets"
            ]
        }
    
    def update_data(self, key: str, value: any) -> None:
        """Actualiza un dato y lo elimina de missing_info si es válido"""
        if key in self.data:
            self.data[key] = value
            if key in self.data["missing_info"]:
                self.data["missing_info"].remove(key)
    
    def update_list_data(self, key: str, values: List[str]) -> None:
        """Actualiza datos de tipo lista"""
        if key in self.data and isinstance(self.data[key], list):
            self.data[key] = values
            if key in self.data["missing_info"]:
                self.data["missing_info"].remove(key)
    
    def get_next_missing_info(self) -> Optional[str]:
        """Obtiene la siguiente información faltante"""
        if self.data["missing_info"]:
            return self.data["missing_info"][0]
        return None
    
    def is_complete(self) -> bool:
        """Verifica si toda la información necesaria ha sido recopilada"""
        return len(self.data["missing_info"]) == 0