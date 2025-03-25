# from langgraph.graph import StateGraph
# from backend.agents.bmi_agent import BMIAgent
# from backend.agents.diet_agent import DietAgent
# from pydantic import BaseModel

# class BMIState(BaseModel):
#     height: float
#     weight: float
#     bmi: float | None = None
#     category: str | None = None
#     diet_recommendation: str | None = None

# graph = StateGraph(BMIState)

# bmi_agent = BMIAgent()
# diet_agent = DietAgent()


# def calculate_bmi(state: BMIState) -> BMIState:
#     bmi_result = bmi_agent.calculate_bmi(state.height, state.weight)
#     if "error" in bmi_result:
#         return state.model_copy(update={"bmi": None, "category": bmi_result["error"]})
#     return state.model_copy(update={"bmi": bmi_result["bmi"], "category": bmi_result["category"]})


# def recommend_diet(state: BMIState) -> BMIState:
#     if state.bmi is None:
#         recommendation = "Cannot recommend diet due to error in BMI calculation."
#     else:
#         recommendation = diet_agent.recommend_diet(state.bmi)
#     return state.model_copy(update={"diet_recommendation": recommendation})

# graph.add_node("calculate_bmi", calculate_bmi)
# graph.add_node("recommend_diet", recommend_diet)

# graph.set_entry_point("calculate_bmi")  # Start with BMI calculation
# graph.add_edge("calculate_bmi", "recommend_diet")  # Then recommend diet
# graph.set_finish_point("recommend_diet")  # Final output includes diet recommendation

# executor = graph.compile()

# if __name__ == "__main__":
#     initial_state = BMIState(height=175, weight=70)
#     final_state = executor.invoke(initial_state)
#     print(final_state)

from langgraph.graph import StateGraph
from backend.models.health_state import HealthState
from backend.agents.bmi_agent import BMIAgent
from backend.agents.diet_agent import DietAgent
from backend.agents.body_type_agent import BodyTypeAgent
from backend.agents.fitness_goal_agent import FitnessGoalAgent
from backend.agents.bp_agent import BPAgent
from backend.agents.sleep_agent import SleepAgent
from backend.agents.chronic_agent import ChronicAgent
from backend.agents.stamina_agent import StaminaAgent
from backend.agents.mental_health_agent import MentalHealthAgent

graph = StateGraph(HealthState)

bmi_agent = BMIAgent()
diet_agent = DietAgent()
body_type_agent = BodyTypeAgent()
fitness_goal_agent = FitnessGoalAgent()
bp_agent = BPAgent()
sleep_agent = SleepAgent()
chronic_agent = ChronicAgent()
stamina_agent = StaminaAgent()
mental_health_agent = MentalHealthAgent()

def calculate_bmi(state: HealthState) -> HealthState:
    bmi_result = bmi_agent.calculate_bmi(state.height, state.weight)
    if "error" in bmi_result:
        return state.model_copy(update={"bmi": None, "category": bmi_result["error"]})
    return state.model_copy(update={
        "bmi": bmi_result["bmi"],
        "category": bmi_result["category"]
    })

def predict_body_type(state: HealthState) -> HealthState:
    result = body_type_agent.predict_body_type(state.bmi, state.activity_level)
    return state.model_copy(update=result)

def predict_fitness_goal(state: HealthState) -> HealthState:
    result = fitness_goal_agent.predict_fitness_goal(state.bmi, state.body_type, state.activity_level, state.diet_preference)
    return state.model_copy(update=result)

def estimate_bp_range(state: HealthState) -> HealthState:
    result = bp_agent.estimate_bp_range(state.age, state.bmi, state.smoking, state.alcohol_intake, state.stress_level, state.activity_level)
    return state.model_copy(update=result)

def predict_sleep_quality(state: HealthState) -> HealthState:
    result = sleep_agent.predict_sleep_quality(state.stress_level, state.alcohol_intake, state.caffeine_intake, state.screen_time)
    return state.model_copy(update=result)

def recommend_diet(state: HealthState) -> HealthState:
    prompt = f"""
    You are an expert nutritionist. Given the following details:
    BMI: {state.bmi}
    Medical Conditions: {state.medical_conditions or 'None'}
    Activity Level: {state.activity_level}
    Diet Preference: {state.diet_preference or 'Standard'}
    Please recommend a detailed diet plan including meal suggestions, portion sizes, macronutrient breakdown, and hydration tips.
    """
    rec = diet_agent.recommend_diet(prompt)
    return state.model_copy(update={"diet_recommendation": rec})

def estimate_chronic_disease_risk(state: HealthState) -> HealthState:
    result = chronic_agent.estimate_chronic_disease_risk(state.family_history, state.bmi, state.smoking, state.alcohol_intake, state.stress_level)
    return state.model_copy(update=result)

def predict_stamina(state: HealthState) -> HealthState:
    result = stamina_agent.predict_stamina(state.age, state.activity_level, state.bmi)
    return state.model_copy(update=result)

def estimate_mental_health(state: HealthState) -> HealthState:
    result = mental_health_agent.estimate_mental_health(state.sleep_quality, state.stress_level, state.family_history)
    return state.model_copy(update=result)

graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node("predict_body_type", predict_body_type)
graph.add_node("predict_fitness_goal", predict_fitness_goal)
graph.add_node("estimate_bp_range", estimate_bp_range)
graph.add_node("predict_sleep_quality", predict_sleep_quality)
graph.add_node("recommend_diet", recommend_diet)
graph.add_node("estimate_chronic_disease_risk", estimate_chronic_disease_risk)
graph.add_node("predict_stamina", predict_stamina)
graph.add_node("estimate_mental_health", estimate_mental_health)

graph.set_entry_point("calculate_bmi")
graph.add_edge("calculate_bmi", "predict_body_type")
graph.add_edge("predict_body_type", "predict_fitness_goal")
graph.add_edge("predict_fitness_goal", "estimate_bp_range")
graph.add_edge("estimate_bp_range", "predict_sleep_quality")
graph.add_edge("predict_sleep_quality", "recommend_diet")
graph.add_edge("recommend_diet", "estimate_chronic_disease_risk")
graph.add_edge("estimate_chronic_disease_risk", "predict_stamina")
graph.add_edge("predict_stamina", "estimate_mental_health")
graph.set_finish_point("estimate_mental_health")

executor = graph.compile()

