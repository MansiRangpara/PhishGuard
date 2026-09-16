# prepare_dataset.py
import pandas as pd
from feature_extractor import extract_features

# Load original CSV
df = pd.read_csv("data.csv")

# Drop rows without label
df = df.dropna(subset=['type'])

# Map labels to binary: 0 = safe, 1 = phishing/malicious
label_mapping = {"benign": 0, "defacement": 1, "phishing": 1, "malware": 1}
df['CLASS_LABEL'] = df['type'].map(label_mapping)

# Extract numeric features
features = df['url'].apply(lambda u: pd.Series(extract_features(u)))
df_features = pd.concat([features, df['CLASS_LABEL']], axis=1)

# Save feature dataset
df_features.to_csv("dataset_features.csv", index=False)
print("Feature dataset saved as dataset_features.csv")
