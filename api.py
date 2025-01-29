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
        print("🔹 Received Data:", df.columns)  # Debugging print
        print("🔹 Model Expected Features:", model.feature_names_in_)  # Debugging print

        # Ensure feature names match
        df = df[model.feature_names_in_]

        prediction = model.predict(df)[0]
        return {"prediction": int(prediction)}
    except Exception as e:
        return {"error": str(e)}

print("✅ API is ready!")
