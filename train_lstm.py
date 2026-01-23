import os
import numpy as np
import pandas as pd
import joblib

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# -------------------------------
# CONFIG
# -------------------------------
DATASET_ROOT = "cloud-monitoring-dataset/data"
SEQ_LEN = 30
EPOCHS = 50
BATCH_SIZE = 128

# -------------------------------
# LOAD ALL CSV FILES
# -------------------------------
csv_files = []

for root, dirs, files in os.walk(DATASET_ROOT):
    for file in files:
        if file.endswith(".csv") and "metadata" not in file:
            csv_files.append(os.path.join(root, file))

print(f"[INFO] Found {len(csv_files)} CSV files")

# -------------------------------
# COLLECT ALL VALUES FIRST
# -------------------------------
all_values = []

for csv in csv_files:
    df = pd.read_csv(csv)

    if not {"TimeStamp", "Value"}.issubset(df.columns):
        continue

    values = pd.to_numeric(df["Value"], errors="coerce")
    values = values.replace([np.inf, -np.inf], np.nan).dropna()

    all_values.extend(values.values)

all_values = np.array(all_values).reshape(-1, 1)

# -------------------------------
# GLOBAL NORMALIZATION
# -------------------------------
scaler = MinMaxScaler()
all_values_scaled = scaler.fit_transform(all_values)
os.makedirs("ml", exist_ok=True)
joblib.dump(scaler, "ml/scaler.pkl")
print("[SUCCESS] Scaler saved as ml/scaler.pkl")
# -------------------------------
# CREATE SEQUENCES
# -------------------------------
sequences = []

for i in range(len(all_values_scaled) - SEQ_LEN):
    seq = all_values_scaled[i : i + SEQ_LEN]
    if not np.any(np.isnan(seq)):
        sequences.append(seq)

X = np.array(sequences)
X = np.expand_dims(X, axis=2)

print("[INFO] Training data shape:", X.shape)

# -------------------------------
# BUILD STABLE LSTM AUTOENCODER
# -------------------------------
inputs = Input(shape=(SEQ_LEN, 1))

encoded = LSTM(
    64,
    activation="tanh",
    return_sequences=False
)(inputs)

decoded = RepeatVector(SEQ_LEN)(encoded)

decoded = LSTM(
    64,
    activation="tanh",
    return_sequences=True
)(decoded)

autoencoder = Model(inputs, decoded)

optimizer = Adam(learning_rate=0.001, clipnorm=1.0)

autoencoder.compile(
    optimizer=optimizer,
    loss="mse"
)

autoencoder.summary()

# -------------------------------
# TRAIN MODEL
# -------------------------------
early_stop = EarlyStopping(
    monitor="loss",
    patience=5,
    restore_best_weights=True
)

history = autoencoder.fit(
    X,
    X,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    shuffle=True,
    callbacks=[early_stop]
)

# -------------------------------
# SAVE MODEL (MODERN FORMAT)
# -------------------------------
autoencoder.save("lstm_anomaly_model.keras")
print("[SUCCESS] Model saved as lstm_anomaly_model.keras")
