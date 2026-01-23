import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
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

# Convert timestamp
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
df = df.sort_values('TimeStamp')

# -------------------------------
# Scale data
# -------------------------------
scaler = MinMaxScaler()
df['Value_scaled'] = scaler.fit_transform(df[['Value']])

# -------------------------------
# Create sequences
# -------------------------------
sequences = []
for i in range(len(df) - SEQ_LEN):
    sequences.append(df['Value_scaled'].values[i:i+SEQ_LEN])

X_test = np.array(sequences)
X_test = X_test.reshape(X_test.shape[0], SEQ_LEN, 1)

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
# Detect anomalies
# -------------------------------
anomalies = mse > threshold
print("[RESULT] Total anomalies detected:", np.sum(anomalies))
