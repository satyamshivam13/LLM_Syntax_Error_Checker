"""
Advanced Model Evaluation Metrics
"""
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    cohen_kappa_score, matthews_corrcoef,
    classification_report, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Load models and data
model = joblib.load('models/error_classifier.pkl')
vectorizer = joblib.load('models/tfidf.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')

df = pd.read_csv('dataset/merged/all_errors.csv')
X = vectorizer.transform(df['buggy_code'])
y_true = label_encoder.transform(df['error_type'])
y_pred = model.predict(X)

print("="*60)
print("ADVANCED EVALUATION METRICS")
print("="*60)

# 1. Cohen's Kappa (inter-rater reliability)
kappa = cohen_kappa_score(y_true, y_pred)
print(f"\nCohen's Kappa Score: {kappa:.4f}")
print("Interpretation:")
if kappa > 0.8:
    print("  ✅ Excellent agreement")
elif kappa > 0.6:
    print("  ✅ Good agreement")
elif kappa > 0.4:
    print("  ⚠️ Moderate agreement")
else:
    print("  ❌ Poor agreement")

# 2. Matthews Correlation Coefficient
mcc = matthews_corrcoef(y_true, y_pred)
print(f"\nMatthews Correlation Coefficient: {mcc:.4f}")
print("Range: -1 (total disagreement) to +1 (perfect prediction)")

# 3. Per-class metrics
print("\n" + "="*60)
print("PER-CLASS DETAILED METRICS")
print("="*60)
precision, recall, f1, support = precision_recall_fscore_support(
    y_true, y_pred, labels=range(len(label_encoder.classes_))
)

metrics_df = pd.DataFrame({
    'Error Type': label_encoder.classes_,
    'Precision': precision,
    'Recall': recall,
    'F1-Score': f1,
    'Support': support
}).sort_values('F1-Score', ascending=False)

print(metrics_df.to_string(index=False))

# 4. Top and Bottom Performers
print("\n" + "="*60)
print("TOP 5 BEST PERFORMING ERROR TYPES")
print("="*60)
print(metrics_df.head(5)[['Error Type', 'F1-Score']].to_string(index=False))

print("\n" + "="*60)
print("TOP 5 NEEDS IMPROVEMENT")
print("="*60)
print(metrics_df.tail(5)[['Error Type', 'F1-Score']].to_string(index=False))

# 5. Error Analysis
print("\n" + "="*60)
print("ERROR ANALYSIS")
print("="*60)
misclassified = np.where(y_true != y_pred)[0]
print(f"Total Misclassifications: {len(misclassified)} / {len(y_true)} ({len(misclassified)/len(y_true)*100:.2f}%)")

# Most confused pairs
cm = confusion_matrix(y_true, y_pred)
confused_pairs = []
for i in range(len(cm)):
    for j in range(len(cm)):
        if i != j and cm[i][j] > 0:
            confused_pairs.append((
                label_encoder.classes_[i],
                label_encoder.classes_[j],
                cm[i][j]
            ))

confused_pairs.sort(key=lambda x: x[2], reverse=True)
print("\nMost Confused Error Pairs:")
for true_label, pred_label, count in confused_pairs[:5]:
    print(f"  {true_label} misclassified as {pred_label}: {count} times")

# 6. Language-wise breakdown
print("\n" + "="*60)
print("LANGUAGE-WISE PERFORMANCE BREAKDOWN")
print("="*60)
for lang in df['language'].unique():
    lang_mask = df['language'] == lang
    lang_true = y_true[lang_mask]
    lang_pred = y_pred[lang_mask]
    
    lang_acc = accuracy_score(lang_true, lang_pred)
    lang_prec, lang_rec, lang_f1, _ = precision_recall_fscore_support(
        lang_true, lang_pred, average='weighted', zero_division=0
    )
    
    print(f"\n{lang}:")
    print(f"  Samples: {sum(lang_mask)}")
    print(f"  Accuracy: {lang_acc:.2%}")
    print(f"  Precision: {lang_prec:.2%}")
    print(f"  Recall: {lang_rec:.2%}")
    print(f"  F1-Score: {lang_f1:.2%}")

# Save detailed report
with open('results/advanced_metrics.txt', 'w') as f:
    f.write("ADVANCED EVALUATION METRICS REPORT\n")
    f.write("="*60 + "\n\n")
    f.write(f"Cohen's Kappa: {kappa:.4f}\n")
    f.write(f"Matthews Correlation Coefficient: {mcc:.4f}\n\n")
    f.write(metrics_df.to_string(index=False))

print("\n✅ Advanced metrics saved to results/advanced_metrics.txt")
