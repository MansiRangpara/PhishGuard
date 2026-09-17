import pandas as pd
from feature_extractor import extract_features


# ---------------------------------------------------------
# Load original dataset
# ---------------------------------------------------------

df = pd.read_csv("data.csv")

print("Original dataset shape:", df.shape)


# ---------------------------------------------------------
# Remove rows without URL or label
# ---------------------------------------------------------

df = df.dropna(subset=["url", "type"])

df["url"] = df["url"].astype(str)
df["type"] = df["type"].astype(str).str.lower().str.strip()


# ---------------------------------------------------------
# Convert labels
#
# 0 = benign
# 1 = malicious
# ---------------------------------------------------------

label_mapping = {
    "benign": 0,
    "phishing": 1,
    "defacement": 1,
    "malware": 1
}

df["CLASS_LABEL"] = df["type"].map(label_mapping)


# Remove unknown labels
df = df.dropna(subset=["CLASS_LABEL"])

df["CLASS_LABEL"] = df["CLASS_LABEL"].astype(int)


# ---------------------------------------------------------
# Extract features
# ---------------------------------------------------------

print("Extracting URL features...")

features = df["url"].apply(
    lambda url: pd.Series(extract_features(url))
)


# ---------------------------------------------------------
# Combine features + labels
# ---------------------------------------------------------

df_features = pd.concat(
    [
        features,
        df["CLASS_LABEL"]
    ],
    axis=1
)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

df_features.to_csv(
    "dataset_features.csv",
    index=False
)


# ---------------------------------------------------------
# Information
# ---------------------------------------------------------

print("\nFeature dataset created successfully.")

print("Feature shape:")
print(df_features.shape)

print("\nClass distribution:")
print(
    df_features["CLASS_LABEL"].value_counts()
)

print("\nFeature columns:")
print(
    df_features.columns.tolist()
)