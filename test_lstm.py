import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tensorflow.keras.models import load_model

# -------------------------------
# CONFIG
# -------------------------------
SEQ_LEN = 30
THRESHOLD_PERCENTILE = 95

# -------------------------------
# Load model
# -------------------------------
model = load_model("lstm_anomaly_model.keras")
print("[INFO] Model loaded")

# -------------------------------
# Load test CSV
# -------------------------------
test_file = "cloud-monitoring-dataset/data/application-crash-rate-1/app1-02.csv"
df = pd.read_csv(test_file)

df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
df = df.sort_values('TimeStamp')

# -------------------------------
# Load training scaler (IMPORTANT)
# -------------------------------
scaler = joblib.load("ml/scaler.pkl")
df['Value_scaled'] = scaler.transform(df[['Value']])

# -------------------------------
# Create sequences
# -------------------------------
sequences = []
window_labels = []

for i in range(len(df) - SEQ_LEN):
    sequences.append(df['Value_scaled'].values[i:i+SEQ_LEN])
    
    # Window label = 1 if ANY anomaly inside window
    label_window = df['Label'].values[i:i+SEQ_LEN]
    window_labels.append(1 if label_window.sum() > 0 else 0)

X_test = np.array(sequences)
X_test = X_test.reshape(X_test.shape[0], SEQ_LEN, 1)

y_true = np.array(window_labels)

print("[INFO] Test data shape:", X_test.shape)

# -------------------------------
# Reconstruction
# -------------------------------
X_pred = model.predict(X_test)

# Reconstruction error
mse = np.mean(np.square(X_test - X_pred), axis=(1, 2))

# -------------------------------
# Threshold
# -------------------------------
threshold = np.percentile(mse, THRESHOLD_PERCENTILE)
print("[INFO] Anomaly threshold:", threshold)

# -------------------------------
# Predictions
# -------------------------------
y_pred = (mse > threshold).astype(int)

print("[RESULT] Total anomalies detected:", np.sum(y_pred))

# -------------------------------
# Evaluation Metrics
# -------------------------------
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("\n===== MODEL PERFORMANCE =====")
print("Accuracy :", acc)
print("Precision:", prec)
print("Recall   :", rec)
print("F1 Score :", f1)
print("\nConfusion Matrix:\n", confusion_matrix(y_true, y_pred))