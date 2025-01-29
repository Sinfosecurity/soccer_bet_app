from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

# Load trained model
try:
    with open('betting_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
    print("🔹 Model Expected Features:", model.feature_names_in_)  # Debugging print
except Exception as e:
    print(f"🔴 Error loading model: {e}")

# Define request body structure
class MatchData(BaseModel):
    team_form: float
    h2h_stats: float
    home_win_rate: float
    away_win_rate: float
@app.post('/predict')
def predict_match(data: MatchData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        # Debugging logs to check model output
        print(f"🔹 Raw Model Prediction (Numeric): {prediction}")

        # Mapping numeric predictions to actual outcomes
        outcome_mapping = {0: "Loss", 1: "Win", 2: "Draw"}
        predicted_outcome = outcome_mapping.get(int(prediction), "Unknown")

        print(f"🔹 Mapped Prediction (Text): {predicted_outcome}")  # Debugging print

        return {"prediction": predicted_outcome}
    except Exception as e:
        return {"error": str(e)}


print("✅ API is ready!")
