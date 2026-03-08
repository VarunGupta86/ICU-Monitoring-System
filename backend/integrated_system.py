import joblib
import numpy as np
import tensorflow as tf
import pandas as pd

# 1. Load All Models
try:
    # Shivam's Models
    xgboost_model = joblib.load('icu_risk_model.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Shanya's Models
    anomaly_model = joblib.load('anomaly_detector.pkl')
    lstm_model = tf.keras.models.load_model('sps_cardiac_lstm.h5')
    
    print("SUCCESS: All 3 AI Engines (XGBoost, LSTM, Anomaly) Loaded Successfully!\n")
except Exception as e:
    print(f"Error loading models: {e}")

def get_comprehensive_report(patient_vitals):
    # Features order (10 features as per your last training)
    features = ['Age', 'Gender', 'Heart Rate (bpm)', 'Oxygen Saturation (%)', 
                'Systolic BP (mmHg)', 'Diastolic BP (mmHg)', 'Body Temperature (°C)', 
                'Derived_HRV', 'Derived_MAP', 'Derived_Pulse_Pressure']
    
    # Preprocessing
    input_df = pd.DataFrame([patient_vitals], columns=features)
    scaled_data = scaler.transform(input_df)
    
    # 1. XGBoost: Current Risk Status (Shivam's)
    risk_idx = xgboost_model.predict(scaled_data)[0]
    risk_label = "CRITICAL" if risk_idx == 0 else "NORMAL"
    
    # 2. Anomaly Detection: Sensor Pattern (Shanya's)
    # Isolation Forest gives -1 for anomaly and 1 for normal
    pattern_idx = anomaly_model.predict(scaled_data)[0]
    pattern_label = "ABNORMAL SENSOR DATA" if pattern_idx == -1 else "STABLE SENSOR DATA"
    
    # 3. LSTM: Future Warning (Shanya's)
    # Reshaping for LSTM: (1 sample, 1 time step, 10 features)
    lstm_input = scaled_data.reshape((1, 1, 10))
    # Note: Using only 1 time step as placeholder; real LSTM needs sequence
    warning_prob = lstm_model.predict(lstm_input, verbose=0)[0][0]
    warning_label = "HIGH ALERT (Potential Cardiac Event)" if warning_prob > 0.5 else "STABLE TREND"

    return {
        "Status": risk_label,
        "Sensor_Check": pattern_label,
        "Cardiac_Prediction": warning_label,
        "Risk_Score": f"{warning_prob * 100:.2f}%"
    }

# --- TEST CASE (Sample Critical Patient) ---
# [Age, Gender, HR, SpO2, SysBP, DiaBP, Temp, HRV, MAP, PP]
critical_sample = [65, 1, 115, 89, 150, 95, 38.5, 0.04, 113, 55]

report = get_comprehensive_report(critical_sample)

print("="*40)
print("       ICU MONITORING FINAL REPORT")
print("="*40)
for key, value in report.items():
    print(f"{key:20}: {value}")
print("="*40)