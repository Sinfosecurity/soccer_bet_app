import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Load and preprocess data
data = pd.read_csv('match_data.csv')  # Ensure match_data.csv exists in your project folder
data = data.dropna()
print("🔹 Data Loaded Successfully")

X = data[['team_form', 'h2h_stats', 'home_win_rate', 'away_win_rate']]
data['match_outcome'] = data['match_outcome'].astype(int)
y = data['match_outcome']

print("🔹 Features Sample:\n", X.head())  # Debugging print
print("🔹 Target Variable Sample:\n", y.head())  # Debugging print

# Split dataset
try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("🔹 Data Split Completed")
except Exception as e:
    print(f"🔴 Error During Data Split: {e}")

# Train logistic regression model
try:
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("🔹 Model Training Completed")
except Exception as e:
    print(f"🔴 Error During Model Training: {e}")

# Evaluate model
try:
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'✅ Model Accuracy: {accuracy * 100:.2f}%')
except Exception as e:
    print(f"🔴 Error During Model Evaluation: {e}")

# Save the trained model
try:
    with open('betting_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Model training complete! Saved as 'betting_model.pkl'")
except Exception as e:
    print(f"🔴 Error Saving Model: {e}")
