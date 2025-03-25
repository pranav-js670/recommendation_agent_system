from pydantic import BaseModel, Field
from typing import Optional

class HealthState(BaseModel):
    height : float = Field(..., gt=0, description="Height in cm") 
    weight : float = Field(..., gt=0, description="Weight in kg")
    age : int = Field(..., gt=0, description="Age in years")
    activity_level : str = Field(..., description="Sedentary, Active, or Highly Active")
    smoking : bool = Field(..., description="True if the person smokes")
    alcohol_intake : str = Field(..., description="None, Moderate, High")
    stress_level : str = Field(..., description="Low, Moderate, High")
    caffeine_intake : str = Field(..., description="None, Low, Moderate, High")
    screen_time : int = Field(..., description="Average daily screen time in hours")
    diet_preference : Optional[str] = Field(None, description="e.g., Vegetarian, Vegan, Non-Vegetarian")
    medical_conditions : Optional[str] = Field(None, description="e.g., Diabetes, Hypertension")
    family_history : Optional[str] = Field(None, description="e.g., Heart Disease, Diabetes")

    bmi : Optional[float] = None
    bmi_category : Optional[str] = None
    body_type : Optional[str] = None
    fitness_goal : Optional[str] = None
    bp_range : Optional[str] = None
    sleep_quality : Optional[str] = None
    diet_recommendation : Optional[str] = None
    chronic_disease_risk : Optional[str] = None
    stamina : Optional[str] = None
    mental_health : Optional[str] = None