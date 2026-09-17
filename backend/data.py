import pandas as pd

# Load the dataset
df = pd.read_csv("data.csv")

# Quick look at the data
print("First 5 rows:")
print(df.head())

# Basic info
print("\nDataset info:")
print(df.info())

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Check class distribution
print("\nClass distribution:")
print(df['type'].value_counts())
