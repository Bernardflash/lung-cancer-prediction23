
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# Create models directory if not exists
os.makedirs('models', exist_ok=True)

# Load data
df = pd.read_csv('data/lung_cancer.csv')

# Preprocessing
df_clean = df.copy()

# Map LUNG_CANCER to 0/1
df_clean['LUNG_CANCER'] = df_clean['LUNG_CANCER'].map({'YES': 1, 'NO': 0})

# Map GENDER to 0/1 (M=1, F=0)
df_clean['GENDER'] = df_clean['GENDER'].map({'M': 1, 'F': 0})

# For other columns with values 1 and 2, shift to 0 and 1
# List of columns to check/transform
cols_to_shift = [col for col in df_clean.columns if col not in ['LUNG_CANCER', 'GENDER', 'AGE']]

for col in cols_to_shift:
    df_clean[col] = df_clean[col] - 1

# Features and Target
X = df_clean.drop('LUNG_CANCER', axis=1)
y = df_clean['LUNG_CANCER']

# Information about features
feature_names = X.columns.tolist()
print("Features:", feature_names)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Model
# Using class_weight='balanced' to handle imbalance
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save Model
joblib.dump(model, 'models/lung_cancer_model.pkl')
print("\nModel saved to models/lung_cancer_model.pkl")

# Save feature names for later use in app
joblib.dump(feature_names, 'models/feature_names.pkl')
