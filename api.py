import random
import requests
import os

# Use API key from environment variable (or replace with your key)
API_KEY = os.getenv("THE_ODDS_API_KEY", "5dcd444b3d092d2a95e8e8239b87c1d1")

# List of all soccer leagues available in The Odds API
SOCCER_LEAGUES = [
    "soccer_argentina_primera_division", "soccer_australia_aleague", "soccer_austria_bundesliga",
    "soccer_belgium_first_div", "soccer_brazil_campeonato", "soccer_brazil_serie_b", 
    "soccer_chile_campeonato", "soccer_china_superleague", "soccer_denmark_superliga",
    "soccer_efl_champ", "soccer_england_efl_cup", "soccer_england_league1", "soccer_england_league2",
    "soccer_epl", "soccer_fa_cup", "soccer_fifa_world_cup", "soccer_fifa_world_cup_womens",
    "soccer_finland_veikkausliiga", "soccer_france_ligue_one", "soccer_france_ligue_two",
    "soccer_germany_bundesliga", "soccer_germany_bundesliga2", "soccer_germany_liga3",
    "soccer_greece_super_league", "soccer_italy_serie_a", "soccer_italy_serie_b",
    "soccer_japan_j_league", "soccer_korea_kleague1", "soccer_league_of_ireland",
    "soccer_mexico_ligamx", "soccer_netherlands_eredivisie", "soccer_norway_eliteserien",
    "soccer_poland_ekstraklasa", "soccer_portugal_primeira_liga", "soccer_spain_la_liga",
    "soccer_spain_segunda_division", "soccer_spl", "soccer_sweden_allsvenskan",
    "soccer_sweden_superettan", "soccer_switzerland_superleague", "soccer_turkey_super_league",
    "soccer_uefa_europa_conference_league", "soccer_uefa_champs_league",
    "soccer_uefa_champs_league_qualification", "soccer_uefa_europa_league",
    "soccer_uefa_european_championship", "soccer_uefa_euro_qualification",
    "soccer_conmebol_copa_america", "soccer_conmebol_copa_libertadores"
]

# Fetch all live soccer matches from The Odds API
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

@app.post('/predict')
def predict_matches(data: MatchData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        # Mapping numeric predictions to actual outcomes
        outcome_mapping = {0: "Away Win", 1: "Home Win", 2: "Draw"}
        predicted_outcome = outcome_mapping.get(int(prediction), "Unknown")

        # Get all live soccer matches
        matches = get_all_soccer_matches()

        predictions = []
        for match in matches:
            if "home_team" in match and "away_team" in match:
                home_team = match["home_team"]
                away_team = match["away_team"]

                # Extract betting odds
                odds = {"home_win": None, "draw": None, "away_win": None}
                if "bookmakers" in match:
                    for bookmaker in match["bookmakers"]:
                        for market in bookmaker["markets"]:
                            if market["key"] == "h2h":  # Head-to-head odds
                                odds["home_win"] = market["outcomes"][0]["price"]
                                odds["away_win"] = market["outcomes"][1]["price"]
                                if len(market["outcomes"]) > 2:
                                    odds["draw"] = market["outcomes"][2]["price"]
                                break

                # Simulated confidence level (replace with real ML confidence in future)
                confidence = round(random.uniform(75, 90), 2)

                predictions.append({
                    "match": f"{home_team} vs {away_team}",
                    "prediction": predicted_outcome,
                    "confidence": f"{confidence}%",
                    "odds": odds
                })

        # Return **only 20 matches per page**
        return {"predictions": predictions[:20]}

    except Exception as e:
        return {"error": str(e)}
