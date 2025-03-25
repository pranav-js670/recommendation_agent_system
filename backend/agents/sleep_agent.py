class SleepAgent:
    def predict_sleep_quality(self, stress_level, alcohol_intake, caffeine_intake, screen_time):
        sl = stress_level.lower() if stress_level else ""
        ai = alcohol_intake.lower() if alcohol_intake else ""
        ci = caffeine_intake.lower() if caffeine_intake else ""
        if sl == "low" and ai == "none" and ci in ["none", "low"]:
            sleep = "7-9 hrs, Good Sleep"
        elif sl == "high" or screen_time > 6:
            sleep = "5-6 hrs, Poor Sleep"
        else:
            sleep = "4-5 hrs, Disturbed Sleep"
        return {"sleep_quality": sleep}
