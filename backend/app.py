# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.services.graph import executor, BMIState

# app = FastAPI()

# class HealthData(BaseModel):
#     height: float
#     weight: float

# @app.post("/predict")
# async def predict_health(data: HealthData):
#     state = BMIState(height=data.height, weight=data.weight)
#     result_state = executor.invoke(state)
#     return result_state

from fastapi import FastAPI
from pydantic import BaseModel
from backend.models.health_state import HealthState
from backend.services.graph import executor
from backend.agents.bmi_agent import BMIAgent
from backend.agents.body_type_agent import BodyTypeAgent
from backend.agents.fitness_goal_agent import FitnessGoalAgent
from backend.agents.bp_agent import BPAgent
from backend.agents.sleep_agent import SleepAgent
from backend.agents.diet_agent import DietAgent
from backend.agents.chronic_agent import ChronicAgent
from backend.agents.stamina_agent import StaminaAgent
from backend.agents.mental_health_agent import MentalHealthAgent

app = FastAPI()

bmi_agent = BMIAgent()
body_type_agent = BodyTypeAgent()
fitness_goal_agent = FitnessGoalAgent()
bp_agent = BPAgent()
sleep_agent = SleepAgent()
diet_agent = DietAgent()
chronic_agent = ChronicAgent()
stamina_agent = StaminaAgent()
mental_health_agent = MentalHealthAgent()

# Request Models for Endpoints

class BMIDate(BaseModel):
    height: float
    weight: float

class BodyTypeDate(BaseModel):
    bmi: float
    activity_level: str

class FitnessGoalData(BaseModel):
    bmi: float
    body_type: str
    activity_level: str
    diet_preference: str | None = None

class BPData(BaseModel):
    age: int
    bmi: float
    smoking: bool
    alcohol_intake: str
    stress_level: str
    activity_level: str

class SleepData(BaseModel):
    stress_level: str
    alcohol_intake: str
    caffeine_intake: str
    screen_time: int

class DietData(BaseModel):
    bmi: float
    medical_conditions: str | None = None
    activity_level: str
    diet_preference: str | None = None

class ChronicData(BaseModel):
    family_history: str | None = None
    bmi: float
    smoking: bool
    alcohol_intake: str
    stress_level: str

class StaminaData(BaseModel):
    age: int
    activity_level: str
    bmi: float

class MentalHealthData(BaseModel):
    sleep_quality: str
    stress_level: str
    family_history: str | None = None

# For the full chained workflow

class FullProfileData(BaseModel):
    height: float
    weight: float
    age: int
    activity_level: str
    smoking: bool
    alcohol_intake: str
    stress_level: str
    caffeine_intake: str
    screen_time: int
    diet_preference: str | None = None
    medical_conditions: str | None = None
    family_history: str | None = None

# Independent API endpoints

@app.post("/predict/bmi")
async def predict_bmi(data: BMIDate):
    result = bmi_agent.calculate_bmi(data.height, data.weight)
    return result

@app.post("/predict/bodytype")
async def predict_body_type(data: BodyTypeDate):
    result = body_type_agent.predict_body_type(data.bmi, data.activity_level)
    return result

@app.post("/predict/fitnessgoal")
async def predict_fitness_goal(data: FitnessGoalData):
    result = fitness_goal_agent.predict_fitness_goal(data.bmi, data.body_type, data.activity_level, data.diet_preference)
    return result

@app.post("/predict/bp")
async def predict_bp(data: BPData):
    result = bp_agent.estimate_bp_range(data.age, data.bmi, data.smoking, data.alcohol_intake, data.stress_level, data.activity_level)
    return result

@app.post("/predict/sleep")
async def predict_sleep(data: SleepData):
    result = sleep_agent.predict_sleep_quality(data.stress_level, data.alcohol_intake, data.caffeine_intake, data.screen_time)
    return result

@app.post("/predict/diet")
async def predict_diet(data: DietData):
    # prompt = f"""
    # You are an expert nutritionist. Given the following details:
    # BMI: {data.bmi}
    # Medical Conditions: {data.medical_conditions or 'None'}
    # Activity Level: {data.activity_level}
    # Diet Preference: {data.diet_preference or 'Standard'}
    # Please recommend a detailed diet plan including meal suggestions, portion sizes, macronutrient breakdown, and hydration tips.
    # """
    prompt = f"""
    You are an expert nutritionist. Given the following details:
    BMI: {data.bmi}
    Medical Conditions: {data.medical_conditions or 'None'}
    Activity Level: {data.activity_level}
    Diet Preference: {data.diet_preference or 'Standard'}
    Please recommend a simple diet style (e.g., "Protein-rich", "Low-carb", "Low-fat") that best suits this profile.
    """
    rec = diet_agent.recommend_diet(prompt)
    return {"diet_recommendation": rec}

@app.post("/predict/chronic")
async def predict_chronic(data: ChronicData):
    result = chronic_agent.estimate_chronic_disease_risk(data.family_history, data.bmi, data.smoking, data.alcohol_intake, data.stress_level)
    return result

@app.post("/predict/stamina")
async def predict_stamina(data: StaminaData):
    result = stamina_agent.predict_stamina(data.age, data.activity_level, data.bmi)
    return result

@app.post("/predict/mentalhealth")
async def predict_mental_health(data: MentalHealthData):
    result = mental_health_agent.estimate_mental_health(data.sleep_quality, data.stress_level, data.family_history)
    return result

# Full chained workflow endpoint

@app.post("/predict/fullprofile")
async def predict_full_profile(data: FullProfileData):
    state = HealthState(**data.model_dump())
    result_state = executor.invoke(state)
    return result_state
