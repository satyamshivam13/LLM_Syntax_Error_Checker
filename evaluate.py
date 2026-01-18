# ============================================================
# Evaluation Script for Multi-Language Syntax Error Checker
# File: evaluate.py
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ------------------------------------------------------------
# 1. Load Dataset
# ------------------------------------------------------------

DATASET_PATH = "dataset/merged/all_errors.csv"

df = pd.read_csv(DATASET_PATH)

print("✅ Dataset Loaded Successfully")
print("Total Samples:", len(df))
print("Languages:", df["language"].unique())
print("Number of Error Types:", df["error_type"].nunique())
print("-" * 60)

# ------------------------------------------------------------
# 2. Prepare Features and Labels
# ------------------------------------------------------------

X = df["buggy_code"]
y = df["error_type"]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("Encoded Error Classes:")
print(list(label_encoder.classes_))
print("-" * 60)

# ------------------------------------------------------------
# 3. Train-Test Split (Stratified)
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    stratify=y_encoded,
    random_state=42
)

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))
print("-" * 60)

# ------------------------------------------------------------
# 4. Feature Extraction (TF-IDF)
# ------------------------------------------------------------

vectorizer = TfidfVectorizer(
    token_pattern=r"[A-Za-z_][A-Za-z0-9_]*",
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("TF-IDF Vectorization Completed")
print("-" * 60)

# ------------------------------------------------------------
# 5. Baseline Model (Logistic Regression)
# ------------------------------------------------------------

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

print("Model Training Completed")
print("-" * 60)

# ------------------------------------------------------------
# 6. Evaluation Metrics
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("🎯 Overall Accuracy:", round(accuracy * 100, 2), "%")
print("\n📊 Classification Report:\n")

print(classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0
))

# ------------------------------------------------------------
# 7. Confusion Matrix
# ------------------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(16, 14))
sns.heatmap(
    cm,
    xticklabels=label_encoder.classes_,
    yticklabels=label_encoder.classes_,
    cmap="Blues",
    annot=False
)

plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix – Multi-Language Error Classification")
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 8. Per-Language Accuracy
# ------------------------------------------------------------

print("\n🌍 Per-Language Accuracy")
print("-" * 40)

for lang in df["language"].unique():
    subset = df[df["language"] == lang]

    X_lang = subset["buggy_code"]
    y_lang = label_encoder.transform(subset["error_type"])

    X_lang_vec = vectorizer.transform(X_lang)
    preds = model.predict(X_lang_vec)

    lang_acc = accuracy_score(y_lang, preds)
    print(f"{lang}: {round(lang_acc * 100, 2)}%")

print("-" * 60)

# ------------------------------------------------------------
# 9. SAVE MODEL FOR APP / CLI (CRITICAL STEP)
# ------------------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/error_classifier.pkl")
joblib.dump(vectorizer, "models/tfidf.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("✅ Model, Vectorizer, and Label Encoder saved in /models")
print("🎉 Evaluation & Model Export Completed Successfully")
