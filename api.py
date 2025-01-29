import random
import requests

@app.post('/predict')
def predict_matches(data: MatchData):
    try:
        df = pd.DataFrame([data.dict()])
        prediction = model.predict(df)[0]

        # Mapping numeric predictions to actual outcomes
        outcome_mapping = {0: "Away Win", 1: "Home Win", 2: "Draw"}
        predicted_outcome = outcome_mapping.get(int(prediction), "Unknown")

        # List of possible matchups
        matches = [
            ("Arsenal", "Man Utd"), ("Chelsea", "Liverpool"), ("Real Madrid", "Barcelona"),
            ("Juventus", "AC Milan"), ("Bayern Munich", "Dortmund"), ("PSG", "Marseille"),
            ("Inter Milan", "Napoli"), ("Atletico Madrid", "Sevilla"), ("Porto", "Benfica"),
            ("Ajax", "Feyenoord"), ("Man City", "Tottenham"), ("Lyon", "Monaco"),
            ("Celtic", "Rangers"), ("Flamengo", "Palmeiras"), ("River Plate", "Boca Juniors"),
            ("LA Galaxy", "New York Red Bulls"), ("Sporting CP", "Braga"), ("RB Leipzig", "Leverkusen"),
            ("Valencia", "Villarreal"), ("Galatasaray", "Fenerbahce")
        ]

        predictions = []
        for home_team, away_team in matches:
            confidence = round(random.uniform(70, 90), 2)  # Generate confidence

            # Only include predictions with confidence ≥ 75%
            if confidence >= 75:
                odds = {
                    "home_win": round(random.uniform(1.5, 2.5), 2),
                    "draw": round(random.uniform(2.8, 3.5), 2),
                    "away_win": round(random.uniform(2.0, 3.5), 2)
                }
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
