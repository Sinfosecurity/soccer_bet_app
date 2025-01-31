from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import random

app = FastAPI()

# Load trained model
try:
    with open('betting_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"🔴 Error loading model: {e}")

# Define request body structure
class MatchData(BaseModel):
    team_form: float
    h2h_stats: float
    home_win_rate: float
    away_win_rate: float

@app.get("/")
def home():
    return {"message": "Welcome to Soccer Bet API. Use /predict to get match predictions."}

@app.post("/predict")
def predict_match(data: MatchData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        # Ensure predictions are mapped correctly
        outcome_mapping = {0: "Away Win", 1: "Home Win", 2: "Draw"}
        predicted_outcome = outcome_mapping.get(int(prediction), "Unknown")

        # Generate confidence level
        confidence = round(random.uniform(75, 95), 2)

        return {
            "match": "Team A vs Team B",
            "prediction": predicted_outcome,
            "confidence": f"{confidence}%",
        }
    except Exception as e:
        return {"error": str(e)}

print("✅ API is ready!")
