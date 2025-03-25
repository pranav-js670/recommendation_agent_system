class StaminaAgent:
    def predict_stamina(self, age, activity_level, bmi):
        if bmi is None:
            return {"stamina": "Unknown"}
        al = activity_level.lower() if activity_level else ""
        if age < 40 and al in ["active", "high", "highly active"]:
            stamina = "High Stamina"
        elif al in ["sedentary", "low"]:
            stamina = "Low Stamina"
        else:
            stamina = "Moderate Stamina"
        return {"stamina": stamina}
