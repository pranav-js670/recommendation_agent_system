class BPAgent:
    def estimate_bp_range(self, age, bmi, smoking, alcohol_intake, stress_level, activity_level):
        if bmi is None:
            return {"bp_range" : "Unknown"}
        al = activity_level.lower() if activity_level else ""
        if age < 40 and bmi < 25 and al in ["active", "high", " highly active"]:
            bp = "110-120/70-80 (Healthy BP)"
        elif bmi >= 25 and al in ["sedentary", "low"] and smoking:
            bp = "130-140/80-90 (Mild Hypertension)"
        elif bmi >= 30 and stress_level.lower() == "high" and alcohol_intake.lower() in ["high", "moderate"]:
            bp = "140+/90+ (Possible Hypertension)"
        else:
            bp = "Normal range"
        return {"bp_range": bp}