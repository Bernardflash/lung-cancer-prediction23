
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data/lung_cancer.csv')

# Basic Info
print("Basic Info:")
print(df.info())
print("\nDescription:")
print(df.describe())
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Target Distribution
print("\nTarget Distribution:")
print(df['LUNG_CANCER'].value_counts())

# Data Cleaning for Correlation (Convert YES/NO to 1/0 and M/F to 1/0)
df_clean = df.copy()
df_clean['LUNG_CANCER'] = df_clean['LUNG_CANCER'].map({'YES': 1, 'NO': 0})
df_clean['GENDER'] = df_clean['GENDER'].map({'M': 1, 'F': 0})

# Correlation Matrix
print("\nCorrelation Matrix:")
corr = df_clean.corr()
print(corr['LUNG_CANCER'].sort_values(ascending=False))
