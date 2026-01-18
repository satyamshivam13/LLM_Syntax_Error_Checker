import joblib
import numpy as np

vectorizer = joblib.load("models/tfidf.pkl")
model = joblib.load("models/error_classifier.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

def detect_error_ml(code: str):
    vec = vectorizer.transform([code])
    probs = model.predict_proba(vec)[0]
    max_prob = float(np.max(probs))
    pred_index = int(np.argmax(probs))
    pred_label = label_encoder.inverse_transform([pred_index])[0]

    return pred_label, max_prob
