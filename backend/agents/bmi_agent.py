class BMIAgent:
    def calculate_bmi(self, height, weight):
        if height <= 0 or weight <= 0:
            return {"error": "Height and weight must be greater than 0"}
        
        
        bmi = weight / ((height / 100) ** 2)
        category = (
            "Underweight" if bmi < 18.5 else
            "Normal weight" if bmi < 25 else
            "Overweight" if bmi < 30 else
            "Obese"
        )
        return {"bmi": round(bmi, 2), "category": category}
