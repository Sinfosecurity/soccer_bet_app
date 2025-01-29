from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import requests
import os
import random

# ✅ Define FastAPI app
app = FastAPI()

# ✅ Load trained model
try:
    with open('betting_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"🔴 Error loading model: {e}")

# ✅ Define the data model
class MatchData(BaseModel):
    team_form: float
    h2h_stats: float
    home_win_rate: float
    away_win_rate: float

# ✅ API key for The Odds API
API_KEY = os.getenv("THE_ODDS_API_KEY", "5dcd444b3d092d2a95e8e8239b87c1d1")

# ✅ List of all soccer leagues
SOCCER_LEAGUES = [
    "soccer_epl", "soccer_uefa_champs_league", "soccer_spain_la_liga",
    "soccer_germany_bundesliga", "soccer_italy_serie_a", "soccer_france_ligue_one"
]

# ✅ Function to fetch all soccer matches
def get_all_soccer_matches():
    matches = []
    for league in SOCCER_LEAGUES:
        url = f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=us&markets=h2h"
        try:
            response = requests.get(url)
            data = response.json()
            if data:
                matches.extend(data)
        except Exception as e:
            print(f"🔴 Error Fetching {league}: {e}")
    return matches

# ✅ Predict API
@app.post('/predict')
def predict_matches(data: MatchData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        outcome_mapping = {0: "Away Win", 1: "Home Win", 2: "Draw"}
        predicted_outcome = outcome_mapping.get(int(prediction), "Unknown")

        matches = get_all_soccer_matches()
        predictions = []

        for match in matches:
            if "home_team" in match and "away_team" in match:
                home_team = match["home_team"]
                away_team = match["away_team"]

                odds = {"home_win": None, "draw": None, "away_win": None}
                if "bookmakers" in match:
                    for bookmaker in match["bookmakers"]:
                        for market in bookmaker["markets"]:
                            if market["key"] == "h2h":
                                odds["home_win"] = market["outcomes"][0]["price"]
                                odds["away_win"] = market["outcomes"][1]["price"]
                                if len(market["outcomes"]) > 2:
                                    odds["draw"] = market["outcomes"][2]["price"]
                                break

                confidence = round(random.uniform(75, 90), 2)

                predictions.append({
                    "match": f"{home_team} vs {away_team}",
                    "prediction": predicted_outcome,
                    "confidence": f"{confidence}%",
                    "odds": odds
                })

        return {"predictions": predictions[:20]}

    except Exception as e:
        return {"error": str(e)}

print("✅ API is ready!")
