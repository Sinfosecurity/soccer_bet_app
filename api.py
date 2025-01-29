import random
import requests

@app.post('/predict')
def predict_match(data: MatchData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        # Mapping numeric predictions to actual outcomes
        outcome_mapping = {0: "Away Win", 1: "Home Win", 2: "Draw"}
        predicted_outcome = outcome_mapping.get(int(prediction), "Unknown")

        # Generate a random matchup
        teams = [
            ("Arsenal", "Man Utd"),
            ("Chelsea", "Liverpool"),
            ("Real Madrid", "Barcelona"),
            ("Juventus", "AC Milan"),
            ("Bayern Munich", "Dortmund")
        ]
        home_team, away_team = random.choice(teams)

        # Simulate confidence level
        confidence = round(random.uniform(65, 85), 2)

        # Simulate odds (this will be replaced with real API calls)
        odds = {
            "home_win": round(random.uniform(1.5, 2.5), 2),
            "draw": round(random.uniform(2.8, 3.5), 2),
            "away_win": round(random.uniform(2.0, 3.5), 2)
        }

        return {
            "match": f"{home_team} vs {away_team}",
            "prediction": predicted_outcome,
            "confidence": f"{confidence}%",
            "odds": odds
        }
    except Exception as e:
        return {"error": str(e)}
