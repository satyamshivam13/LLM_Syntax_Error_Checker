"""
Generate results.csv for visualization from evaluation
"""
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("dataset/merged/all_errors.csv")

# Load trained models
model = joblib.load("models/error_classifier.pkl")
vectorizer = joblib.load("models/tfidf.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# Prepare features
X = df["buggy_code"]
y = df["error_type"]

# Transform features
X_vec = vectorizer.transform(X)

# Get predictions
y_pred_encoded = model.predict(X_vec)
y_pred = label_encoder.inverse_transform(y_pred_encoded)

# Create results dataframe
results_df = pd.DataFrame({
    'code': df['buggy_code'].values,
    'language': df['language'].values,
    'error_type': df['error_type'].values,
    'predicted': y_pred
})

# Save to CSV
os.makedirs("data", exist_ok=True)
results_df.to_csv("data/results.csv", index=False)

print(f"✅ Generated data/results.csv with {len(results_df)} samples")
print(f"Columns: {list(results_df.columns)}")
