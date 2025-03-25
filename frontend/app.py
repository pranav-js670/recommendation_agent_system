# import streamlit as st
# import requests

# st.set_page_config(page_title="AI Health Predictor", layout="centered")

# st.title("🤖 AI Health Predictor")

# height = st.number_input("Enter height in centimeters", min_value=50.0, max_value=250.0, step=0.1, format="%.2f")
# weight = st.number_input("Enter weight in kg", min_value=1.0, max_value=500.0, step=0.1, format="%.2f")

# data = {"height": height, "weight": weight}

# st.write(f"Sending data: {data}")

# if st.button("Predict"):
#     response = requests.post(
#         "http://127.0.0.1:8000/predict",
#         json=data
#     )
    
#     try:
#         result = response.json()
#         if "bmi" in result and "category" in result:
#             st.success(f"BMI: {result['bmi']} ({result['category']})")
#             st.subheader("Diet Recommendation")
#             st.write(result.get("diet_recommendation", "No recommendation available."))
#         else:
#             st.error("Unexpected response format!")
    
#     except requests.exceptions.JSONDecodeError:
#         st.error("Error: Could not parse server response. Check the backend.")

import streamlit as st
import requests

st.set_page_config(page_title="AI Health Predictor", layout="centered")
st.title("🤖 AI Health Predictor")

# Option to choose between full profile and step-by-step individual predictions
mode = st.selectbox("Select Mode", options=["Full Profile", "Step-by-Step Predictions"])

if mode == "Full Profile":
    st.header("Complete Health Profile Prediction")
    height = st.number_input("Enter height (cm)", min_value=50.0, max_value=250.0, step=0.1)
    weight = st.number_input("Enter weight (kg)", min_value=1.0, max_value=500.0, step=0.1)
    age = st.number_input("Enter age", min_value=1, max_value=120, step=1)
    activity_level = st.selectbox("Activity Level", options=["Sedentary", "Active", "Highly Active"])
    smoking = st.checkbox("Do you smoke?")
    alcohol_intake = st.selectbox("Alcohol Intake", options=["None", "Moderate", "High"])
    stress_level = st.selectbox("Stress Level", options=["Low", "Moderate", "High"])
    caffeine_intake = st.selectbox("Caffeine Intake", options=["None", "Low", "Moderate", "High"])
    screen_time = st.number_input("Daily Screen Time (hrs)", min_value=0, max_value=24, step=1)
    diet_preference = st.text_input("Diet Preference (Optional)")
    medical_conditions = st.text_input("Medical Conditions (Optional)")
    family_history = st.text_input("Family History (Optional)")
    
    if st.button("Predict Full Profile"):
        data = {
            "height": height,
            "weight": weight,
            "age": age,
            "activity_level": activity_level,
            "smoking": smoking,
            "alcohol_intake": alcohol_intake,
            "stress_level": stress_level,
            "caffeine_intake": caffeine_intake,
            "screen_time": screen_time,
            "diet_preference": diet_preference or None,
            "medical_conditions": medical_conditions or None,
            "family_history": family_history or None
        }
        response = requests.post("http://127.0.0.1:8000/predict/full", json=data)
        st.json(response.json())

elif mode == "Step-by-Step Predictions":
    st.header("Step-by-Step Health Predictions")

    st.subheader("1: BMI Prediction")
    height = st.number_input("Enter height (cm)", min_value=50.0, max_value=250.0, step=0.1)    
    weight = st.number_input("Enter weight (kg)", min_value=1.0, max_value=500.0, step=0.1)
    if st.button("Predict BMI"):
        data = {"height": height, "weight": weight}
        response = requests.post("http://127.0.0.1:8000/predict/bmi", json=data)
        result = response.json()
        if "error" in result:
            st.error(result["error"])
        else:
            st.session_state["bmi"] = result.get("bmi")
            st.session_state["bmi_category"] = result.get("category")
            st.success(f"BMI: {st.session_state['bmi']} ({st.session_state['bmi_category']})")

        st.subheader("2: Body Type Prediction")
        if "bmi" in st.session_state:
            st.write(f"Using computed BMI: {st.session_state['bmi']}")
        activity_level = st.selectbox("Select Activity Level", options=["Sedentary", "Active", "Highly Active"], key="activity_level")
        if st.button("Predict Body Type"):
            data = {"bmi": st.session_state["bmi"], "activity_level": activity_level}
            response = requests.post("http://127.0.0.1:8000/predict/bodytype", json=data)
            result = response.json()
            st.session_state["body_type"] = result.get("body_type")
            st.success(f"Body Type: {st.session_state['body_type']}")
        else:
            st.warning("Please predict BMI first!")

        st.subheader("Step 3: Fitness Goal Prediction")
        if "bmi" in st.session_state and "body_type" in st.session_state:
            activity_level = st.selectbox("Confirm Activity Level", options=["Sedentary", "Active", "Highly Active"], key="activity_level_fit")
        diet_preference = st.text_input("Diet Preference (Optional)", key="diet_pref")
        if st.button("Predict Fitness Goal"):
            data = {
                "bmi": st.session_state["bmi"],
                "body_type": st.session_state["body_type"],
                "activity_level": activity_level,
                "diet_preference": diet_preference or None
            }
            response = requests.post("http://127.0.0.1:8000/predict/fitnessgoal", json=data)
            result = response.json()
            st.session_state["fitness_goal"] = result.get("fitness_goal")
            st.success(f"Fitness Goal: {st.session_state['fitness_goal']}")
        else:
            st.warning("Please complete previous steps first!")
    
    # Step 4: Blood Pressure Range Prediction
    st.subheader("Step 4: Blood Pressure Range Prediction")
    if "bmi" in st.session_state:
        age = st.number_input("Enter Age", min_value=1, max_value=120, step=1, key="age_bp")
        smoking = st.checkbox("Do you smoke?", key="smoking_bp")
        alcohol_intake = st.selectbox("Alcohol Intake", options=["None", "Moderate", "High"], key="alcohol_bp")
        stress_level = st.selectbox("Stress Level", options=["Low", "Moderate", "High"], key="stress_bp")
        activity_level_bp = st.selectbox("Activity Level", options=["Sedentary", "Active", "Highly Active"], key="activity_bp")
        if st.button("Predict BP Range"):
            data = {
                "age": age,
                "bmi": st.session_state["bmi"],
                "smoking": smoking,
                "alcohol_intake": alcohol_intake,
                "stress_level": stress_level,
                "activity_level": activity_level_bp
            }
            response = requests.post("http://127.0.0.1:8000/predict/bp", json=data)
            result = response.json()
            st.session_state["bp_range"] = result.get("bp_range")
            st.success(f"BP Range: {st.session_state['bp_range']}")
    else:
        st.warning("Please predict BMI first!")
    
