# train.py
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load features dataset
df = pd.read_csv("dataset_features.csv")

# Split features and labels
X = df.drop("CLASS_LABEL", axis=1)
y = df["CLASS_LABEL"]

# Class imbalance handling
neg, pos = (y==0).sum(), (y==1).sum()
scale_pos_weight = neg / pos
print(f"Scale pos weight: {scale_pos_weight:.2f}")

# Split into training and validation
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train XGBoost model
model = xgb.XGBClassifier(
    n_estimators=1000,
    max_depth=5,
    learning_rate=0.05,
    tree_method='hist',
    scale_pos_weight=scale_pos_weight,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_val)
print("Confusion Matrix:\n", confusion_matrix(y_val, y_pred))
print("\nClassification Report:\n", classification_report(y_val, y_pred))

# Save model
joblib.dump(model, "phishing_model_final.pkl")
print("Model saved as phishing_model_final.pkl")
