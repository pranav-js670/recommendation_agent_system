class MentalHealthAgent:
    def estimate_mental_health(self, sleep_quality, stress_level, family_history):
        if not sleep_quality:
            return {"mental_health": "Undefined"}
        sl = stress_level.lower() if stress_level else ""
        if "good" in sleep_quality.lower() and sl == "low":
            mh = "Low Stress Risk"
        elif sl == "high":
            mh = "High Stress Risk"
        else:
            mh = "Moderate Stress Risk"
        return {"mental_health": mh}
