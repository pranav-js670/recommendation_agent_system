# from backend.models.llm_model import LLMModel

# class DietAgent:
#     def __init__(self):
#         self.llm = LLMModel()

#     def recommend_diet(self, bmi):
#         prompt = f"""
#         You are an expert nutritionist. A user has a BMI of {bmi}, Recommend a highly detailed meal plan, including:
#         - Breakfast, Lunch, Dinner
#         - Suggested portion sizes
#         - Macronutrient breakdown
#         - Hydration tips
#         """

#         return self.llm.generate_response(prompt)

from backend.models.llm_model import LLMModel

class DietAgent:
    def __init__(self):
        self.llm = LLMModel()

    def recommend_diet(self, prompt: str) -> str:
        return self.llm.generate_response(prompt)