class FitnessGoalAgent:
    def predict_fitness_goal(self, bmi, body_type, activity_level, diet_perference=None):
        if bmi  is None or body_type is None or activity_level is None:
            return {"fitness_goal":"Undefined"}
        if bmi < 18.5:
            goal = "Weight Gain, Muscle Building"
        elif 18.5 <= bmi < 24.9:
            goal = "Strength Training, Endurance" if activity_level.lower() in ["active", "high", "highly active"] else "Maintain Weight"
        else:
            goal = "Weight Loss, Fat Reduction"
        return {"fitness_goal": goal}