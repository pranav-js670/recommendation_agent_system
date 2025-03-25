class ChronicAgent:
    def estimate_chronic_disease_risk(self, family_history, bmi, smoking, alcohol_intake, stress_level):
        if bmi is None:
            risk = "Unknown"
        else:
            if bmi >= 30 or (smoking and family_history and "diabetes" in family_history.lower()):
                risk = "Elevated risk for chronic diseases"
            else:
                risk = "Low to moderate risk"
        return {"chronic_disease_risk": risk}
