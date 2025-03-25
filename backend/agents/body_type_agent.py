class BodyTypeAgent:
    def predict_body_type(self, bmi, activity_level):
        if bmi is None:
            body_type = "Unknown"
        elif activity_level is None:
            body_type = "Unknown"
        else:
            al = activity_level.lower()
            if bmi < 18.5:
                body_type = "Lean/Thin" if al in ["sedentary", "low"] else "Normal"
            elif 18.5 <= bmi < 24.9:
                body_type = "Athletic build" if al in ["active", "high", "highly active"] else "Normal"
            else:  # state.bmi >= 25
                if al in ["sedentary", "low"]:
                    body_type = "Heavy build"
                elif al in ["very active", "high", "highly active"]:
                    body_type = "Muscular but heavy"
                else:
                    body_type = "Overweight"
        return {"body_type": body_type}