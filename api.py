from fastapi import FastAPI
import requests
import pickle
import pandas as pd
import datetime
import random

app = FastAPI()

# Load trained model
try:
    with open('betting_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"🔴 Error loading model: {e}")

# ✅ Function to fetch upcoming matches from Odds API
def get_all_soccer_matches():
    API_KEY = "YOUR_API_KEY_HERE"
    SPORTS = [
        "soccer_epl", "soccer_spain_la_liga", "soccer_italy_serie_a", 
        "soccer_germany_bundesliga", "soccer_france_ligue_one", "soccer_uefa_champs_league"
    ]
    url = f"https://api.the-odds-api.com/v4/sports/"
    matches = []
    
    for sport in SPORTS:
        response = requests.get(f"{url}{sport}/odds", params={"apiKey": API_KEY, "regions": "eu"})
        if response.status_code == 200:
            data = response.json()
            for match in data:
                match["league"] = sport  # Add league name to match data
                matches.append(match)
    
    return matches

# ✅ Predict API - Sort by Odds & Return as Table
@app.post('/predict')
def predict_matches():
    try:
        matches = get_all_soccer_matches()
        predictions_by_date = {}

        for match in matches:
            if "home_team" in match and "away_team" in match and "commence_time" in match:
                home_team = match["home_team"]
                away_team = match["away_team"]
                match_date = datetime.datetime.fromisoformat(match["commence_time"]).strftime("%m/%d/%Y")
                league = match["league"]

                # Extract odds
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

                # Generate confidence level randomly (to be replaced with actual calculation)
                confidence = round(random.uniform(75, 90), 2)

                # Dummy prediction (replace with actual model prediction)
                prediction = random.choice(["Home Win", "Away Win", "Draw"])

                # Select correct odds based on prediction
                predicted_odds = None
                if prediction == "Home Win":
                    predicted_odds = odds["home_win"]
                elif prediction == "Away Win":
                    predicted_odds = odds["away_win"]
                elif prediction == "Draw":
                    predicted_odds = odds["draw"]

                match_prediction = {
                    "league": league,
                    "match": f"{home_team} vs {away_team}",
                    "prediction": prediction,
                    "odds": predicted_odds,
                    "confidence": f"{confidence}%"
                }

                # Group by date
                if match_date not in predictions_by_date:
                    predictions_by_date[match_date] = []
                predictions_by_date[match_date].append(match_prediction)

        # ✅ Sort matches for each date by the best odds (lowest odds first)
        for date in predictions_by_date:
            predictions_by_date[date].sort(key=lambda x: (x["odds"] is not None, x["odds"]))

        # ✅ Convert to table format
        results = {}
        for date, matches in predictions_by_date.items():
            results[date] = pd.DataFrame(matches)

        return results

    except Exception as e:
        return {"error": str(e)}

print("✅ API is ready!")
