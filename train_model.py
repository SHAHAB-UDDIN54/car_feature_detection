import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Dataset Loading
excel_path = "car_feature.xlsx"

if os.path.exists(excel_path):
    print(f"Loading dataset from '{excel_path}'...")
    df = pd.read_excel(excel_path)
else:
    raise FileNotFoundError(f"Dataset '{excel_path}' not found!")

# Strip column names
df.columns = [c.strip() for c in df.columns]

# Ensure required columns exist
required_cols = ["Brand", "Model", "Engine_cc", "Fuel_type", "Color", "Condition", "Transmission", "Mileage", "Price"]
for col in required_cols:
    if col not in df.columns:
        raise KeyError(f"Missing column '{col}' in dataset. Available: {df.columns.tolist()}")

X = df.drop("Price", axis=1)
Y = df["Price"]

categorical_features = ["Brand", "Fuel_type", "Color", "Condition", "Transmission"]
numeric_features = ["Model", "Engine_cc", "Mileage"]

# Preprocessor for categorical and numerical features
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ("num", StandardScaler(), numeric_features)
    ]
)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Evaluate Models
models = {
    "Random Forest": RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=150, learning_rate=0.05, max_depth=6, random_state=42),
    "Linear Regression": LinearRegression()
}

best_model_name = None
best_model_pipe = None
best_r2 = -float("inf")

print("\n--- Model Evaluation ---")
for name, model in models.items():
    pipe = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])
    pipe.fit(X_train, Y_train)
    preds = pipe.predict(X_test)
    
    mae = mean_absolute_error(Y_test, preds)
    rmse = np.sqrt(mean_squared_error(Y_test, preds))
    r2 = r2_score(Y_test, preds)
    print(f"{name:18s} -> MAE: PKR {mae:,.0f} | RMSE: PKR {rmse:,.0f} | R2: {r2:.4f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model_name = name
        best_model_pipe = pipe

print(f"\nBest performing model: {best_model_name} (R2 Score: {best_r2:.4f})")

# Fit final model on full dataset
final_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42))
])

final_pipeline.fit(X, Y)

model_filename = "car_price_model.pkl"
joblib.dump(final_pipeline, model_filename)
print(f"Pipeline model successfully trained and saved to '{model_filename}'")
