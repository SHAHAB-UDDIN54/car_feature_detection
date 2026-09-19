# 🚗 Car Price & Feature Detection — Developer Guide

A concise, to-the-point guide explaining **all features**, **how they work**, and the **step-by-step process** for Project Managers and Developers.

---

## 🔄 Overall System Process Flow

```
1. Image Input        2. Feature Scan       3. Form Auto-Fill       4. Price Prediction     5. Result Display
[ Camera / Upload ] ➔ [ 5-Stage Scan ]   ➔ [ Detected Badges ]  ➔ [ Valuation Formula ] ➔ [ PKR Price + Specs ]
```

---

## 📌 Feature 1: Image Input (Camera & Upload)

### What it does:
Allows the user to provide a car photo using either their device camera or an existing image file.

### How it works:
- **Take Photo (Camera)**:
  1. User clicks **"Take Photo"**.
  2. Browser opens live webcam/phone camera modal (`navigator.mediaDevices.getUserMedia`).
  3. User clicks **"Capture Photo"**.
  4. System draws video frame on an HTML5 canvas and converts it to a JPEG image.
  5. Camera stream turns off and image preview appears.
- **Upload Image (Gallery)**:
  1. User clicks **"Upload Image"**.
  2. Native file dialog opens to pick a `.jpg` or `.png` file.
  3. `FileReader` converts the file to a displayable preview.
- **Remove Image**:
  - Clicking `✕` removes the photo and resets detected features.

---

## 📌 Feature 2: Automated Feature Detection

### What it does:
Scans the uploaded image and extracts 8 car specifications with a visual loading progress indicator.

### How it works:
1. When an image is captured or uploaded, the system starts scanning automatically.
2. An animated **progress bar** updates through 5 stages:
   - **20%**: Analyzing image quality
   - **40%**: Detecting car brand and model
   - **60%**: Identifying engine and specs
   - **80%**: Calculating market value
   - **100%**: Analysis complete
3. Extracts 8 parameters:
   - **Brand**: (e.g. Toyota, Honda, Suzuki, Mercedes, BMW, Audi)
   - **Model Year**: (e.g. 2015 – 2024)
   - **Engine Capacity**: (e.g. 1300, 1500, 1800 CC)
   - **Fuel Type**: (Petrol, Diesel, Hybrid, Electric)
   - **Color**: (White, Black, Silver, etc.)
   - **Condition**: (New, Used)
   - **Transmission**: (Automatic, Manual)
   - **Mileage**: (e.g. 45,000 KM)

---

## 📌 Feature 3: Form Auto-Fill & Manual Override

### What it does:
Transfers detected specs into the form while letting the user review or change any field.

### How it works:
1. **Auto-Fill**:
   - Each input/dropdown in the form is automatically filled with detected values.
2. **Visual Badges**:
   - Input borders turn green (`.detected`).
   - A green **"✓ Detected"** badge appears next to each label.
3. **Manual Override**:
   - If any value is inaccurate or needs changing, the user can manually edit any field.
   - The user can also manually type details without uploading an image and click **"Analyze Image & Predict Price"**.

---

## 📌 Feature 4: Price Prediction Engine

### What it does:
Calculates the estimated market price in **PKR (Pakistani Rupees)** based on car specifications.

### How it works:
1. Starts from a **Base Price**: `PKR 1,000,000`.
2. Multiplies by specific car factors:
   - **Brand Factor**: Mercedes (2.5x), BMW (2.4x), Audi (2.3x), Toyota (1.2x), Honda (1.15x), Suzuki (1.0x), etc.
   - **Year Factor**: Newer cars get higher value `(Year - 2010) * 8%`.
   - **Engine Factor**: Scaled by engine size `(Engine CC / 1800)`.
   - **Fuel Factor**: Electric (1.3x), Hybrid (1.2x), Diesel (1.1x), Petrol (1.0x).
   - **Condition Factor**: New (1.3x), Used (1.0x).
   - **Transmission Factor**: Automatic (1.15x), Manual (1.0x).
   - **Mileage Factor**: Depreciates with higher mileage: `1 - (Mileage / 200,000)` (minimum 40%).
   - **Market Variance**: Adds realistic ±10% market variation.
3. **Result Display**:
   - Smoothly scrolls to the **Estimated Price** card.
   - Shows price formatted in PKR (e.g., `PKR 3,450,000`).
   - Displays a summary box with all detected car features as pills.

---

## 📌 Feature 5: ML Training Pipeline (`train_model.py`)

### What it does:
A data science script to train a Machine Learning model using historical car data (`car_feature.xlsx`).

### How it works:
1. **Load Data**: Reads `car_feature.xlsx` with Pandas.
2. **Preprocessing**:
   - Categorical fields (`Brand`, `Fuel_type`, `Color`, `Condition`, `Transmission`) ➔ One-Hot Encoded.
   - Numerical fields (`Model`, `Engine_cc`, `Mileage`) ➔ Standard Scaled.
3. **Model Evaluation**:
   - Tests **Random Forest**, **XGBoost**, and **Linear Regression**.
   - Calculates **MAE**, **RMSE**, and **$R^2$ Score** on an 80/20 train-test split.
4. **Export**:
   - Saves the best trained pipeline to `car_price_model.pkl` using `joblib`.

---

## 📋 Current Status & Next Steps for Project Manager

| Component | Current State | Next Action Required |
| :--- | :--- | :--- |
| **Frontend (`index.html`)** | ✅ Fully working UI with camera, upload, progress animation, auto-fill, and price calculation. | Ready. |
| **Backend (`app.py`)** | ⚠️ Empty file (0 bytes). | Create Flask/FastAPI server to connect frontend with ML model and Vision AI. |
| **Dataset (`car_feature.xlsx`)** | ⚠️ 9 rows, prices written as strings (`'4.19core'`, `'28.74lacs'`). | Convert string prices to numbers and expand records. |
| **ML Model (`train_model.py`)** | ⚠️ Ready to train once dataset column names and numbers are updated. | Run training and generate `car_price_model.pkl`. |
| **AI Vision** | ⚠️ Currently simulates detection in JavaScript. | Connect to real Computer Vision API (YOLO or Gemini Vision API). |
