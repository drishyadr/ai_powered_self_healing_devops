import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

SEQ_LEN = 30

MODEL_PATH = "ml/memory_lstm_model.keras"
SCALER_PATH = "ml/memory_scaler.pkl"

TRAIN_DATASET = "data/all_cpu_features_no_load_memory_features_no_load.csv"
TEST_DATASET = "data/all_cpu_features_high_load_memory_features_high_load.csv"

print("[INFO] Loading model and scaler...")

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# -------------------------------------------------
# Function to create sequences
# -------------------------------------------------

def create_sequences(data, seq_len):
    sequences = []
    for i in range(len(data) - seq_len):
        sequences.append(data[i:i+seq_len])
    return np.array(sequences)

# -------------------------------------------------
# LOAD TRAIN DATA (NORMAL DATA)
# -------------------------------------------------

print("[INFO] Loading training dataset (normal)...")

train_df = pd.read_csv(TRAIN_DATASET)

train_values = train_df["memory_used_bytes"].values.reshape(-1,1)

train_scaled = scaler.transform(train_values)

X_train = create_sequences(train_scaled, SEQ_LEN)

print("Train shape:", X_train.shape)

# -------------------------------------------------
# COMPUTE TRAIN RECONSTRUCTION ERROR
# -------------------------------------------------

train_recon = model.predict(X_train)

train_mse = np.mean(np.square(X_train - train_recon), axis=(1,2))

threshold = np.mean(train_mse) + 3 * np.std(train_mse)

print("\n[INFO] Threshold computed from training data")
print("Mean MSE :", np.mean(train_mse))
print("Std MSE  :", np.std(train_mse))
print("Threshold:", threshold)

# -------------------------------------------------
# LOAD TEST DATA (HIGH LOAD)
# -------------------------------------------------

print("\n[INFO] Loading test dataset (high load)...")

test_df = pd.read_csv(TEST_DATASET)

test_values = test_df["memory_used_bytes"].values.reshape(-1,1)

test_scaled = scaler.transform(test_values)

X_test = create_sequences(test_scaled, SEQ_LEN)

print("Test shape:", X_test.shape)

# -------------------------------------------------
# CREATE GROUND TRUTH LABELS
# -------------------------------------------------

# Memory threshold rule (example: >700MB considered anomaly)
memory_threshold = 700 * 1024 * 1024

labels = (test_values.flatten() > memory_threshold).astype(int)

# Convert labels into window labels
y_true = []

for i in range(len(labels) - SEQ_LEN):

    if labels[i:i+SEQ_LEN].sum() > 0:
        y_true.append(1)
    else:
        y_true.append(0)

y_true = np.array(y_true)

# -------------------------------------------------
# PREDICTION
# -------------------------------------------------

test_recon = model.predict(X_test)

test_mse = np.mean(np.square(X_test - test_recon), axis=(1,2))

y_pred = (test_mse > threshold).astype(int)

# -------------------------------------------------
# METRICS
# -------------------------------------------------

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# -------------------------------------------------
# RESULTS
# -------------------------------------------------

print("\nEvaluation Metrics")
print("-------------------")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

# -------------------------------------------------
# ANOMALY STATISTICS
# -------------------------------------------------

num_anomalies = np.sum(y_pred)

print("\n[ANOMALY DETECTION RESULTS]")
print("---------------------------")
print("Total windows tested :", len(y_pred))
print("Detected anomalies   :", num_anomalies)
print("Anomaly percentage   :", (num_anomalies / len(y_pred)) * 100)

# -------------------------------------------------
# SHOW SOME ANOMALY INDICES
# -------------------------------------------------

anomaly_indices = np.where(y_pred == 1)[0]

print("\nFirst 10 anomaly indices:")
print(anomaly_indices[:10])
