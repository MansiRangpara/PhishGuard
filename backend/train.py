import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score
)

import joblib


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

df = pd.read_csv("dataset_features.csv")

print("Dataset shape:", df.shape)


# ---------------------------------------------------------
# Separate X and y
# ---------------------------------------------------------

X = df.drop(
    "CLASS_LABEL",
    axis=1
)

y = df["CLASS_LABEL"]


# ---------------------------------------------------------
# Check classes
# ---------------------------------------------------------

print("\nClass distribution:")
print(y.value_counts())


# ---------------------------------------------------------
# Class imbalance
# ---------------------------------------------------------

negative = (y == 0).sum()
positive = (y == 1).sum()

scale_pos_weight = negative / positive

print(
    f"\nScale pos weight: {scale_pos_weight:.4f}"
)


# ---------------------------------------------------------
# Train / validation split
# ---------------------------------------------------------

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------------
# XGBoost
# ---------------------------------------------------------

model = xgb.XGBClassifier(

    n_estimators=500,

    max_depth=5,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    tree_method="hist",

    scale_pos_weight=scale_pos_weight,

    objective="binary:logistic",

    eval_metric="logloss",

    n_jobs=-1,

    random_state=42
)


# ---------------------------------------------------------
# Train
# ---------------------------------------------------------

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# Predictions
# ---------------------------------------------------------

y_pred = model.predict(X_val)

y_prob = model.predict_proba(X_val)[:, 1]


# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------

accuracy = accuracy_score(
    y_val,
    y_pred
)

auc = roc_auc_score(
    y_val,
    y_prob
)

print("\n==============================")
print("MODEL RESULTS")
print("==============================")

print(
    f"\nAccuracy: {accuracy:.4f}"
)

print(
    f"ROC-AUC: {auc:.4f}"
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_val,
        y_pred
    )
)


print("\nClassification Report:")

print(
    classification_report(
        y_val,
        y_pred,
        digits=4
    )
)


# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------

joblib.dump(
    model,
    "phishing_model_final.pkl"
)

print(
    "\nModel saved as phishing_model_final.pkl"
)