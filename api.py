from fastapi import FastAPI
from pydantic import BaseModel
import requests
import random
import pickle
import pandas as pd
import os

app = FastAPI()

# ✅ Load trained model
try:
    with open("betting_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"🔴 Error loading model: {e}")

# ✅ Define request body structure
class MatchData(BaseModel):
    team_form: float
    h2h_stats: float
    home_win_rate: float
    away_win_rate: float

# ✅ Function to fetch soccer matches from The Odds API
def get_all_soccer_matches():
    API_KEY = "5dcd444b3d092d2a95e8e8239b87c1d1"
    SPORTS = ["soccer_epl", "soccer_spain_la_liga", "soccer_italy_serie_a"]  # Add more leagues as needed
    matches = []

    for sport in SPORTS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": "us",  # Can be "us", "uk", "eu"
            "markets": "h2h",  # Head-to-head odds
            "oddsFormat": "decimal"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            matches.extend(response.json())
        else:
            print(f"❌ Error fetching {sport}: {response.status_code} - {response.text}")

    return matches

# ✅ Predict API
@app.post("/predict")
def predict_matches():
    try:
        matches = get_all_soccer_matches()
        predictions = []

        for match in matches:
            if "home_team" in match and "away_team" in match:
                home_team = match["home_team"]
                away_team = match["away_team"]

                # ✅ Extract odds properly
                odds = {"home_win": None, "draw": None, "away_win": None}
                if "bookmakers" in match:
                    for bookmaker in match["bookmakers"]:
                        for market in bookmaker["markets"]:
                            if market["key"] == "h2h":
                                try:
                                    odds["home_win"] = float(market["outcomes"][0]["price"])
                                    odds["away_win"] = float(market["outcomes"][1]["price"])
                                    if len(market["outcomes"]) > 2:
                                        odds["draw"] = float(market["outcomes"][2]["price"])
                                except (IndexError, ValueError):
                                    print(f"⚠️ Error extracting odds for {home_team} vs {away_team}")
                                break  # ✅ Stop looping once we get the odds

                # ✅ Simulating model prediction (Replace with real model input)
                prediction = random.choice(["Home Win", "Away Win", "Draw"])
                confidence = round(random.uniform(75, 90), 2)

                # ✅ Add to predictions if confidence is high
                if confidence >= 75:
                    predictions.append({
                        "match": f"{home_team} vs {away_team}",
                        "prediction": prediction,
                        "confidence": f"{confidence}%",
                        "odds": odds
                    })

        return {"predictions": predictions[:20]}  # ✅ Limit to 20 matches

    except Exception as e:
        return {"error": str(e)}

print("✅ API is ready!")
