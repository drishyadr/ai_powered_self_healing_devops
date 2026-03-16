import os
import numpy as np
import pandas as pd
import joblib

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

SEQ_LEN = 30
EPOCHS = 50
BATCH_SIZE = 128

DATASET = "data/all_cpu_features_no_load_memory_features_no_load.csv"

print("[INFO] Loading dataset...")

df = pd.read_csv(DATASET)

print("[INFO] Columns:", df.columns)

# use memory column
values = df["memory_used_bytes"].values.reshape(-1,1)

# -------------------------------
# NORMALIZE
# -------------------------------

scaler = MinMaxScaler()
values_scaled = scaler.fit_transform(values)

os.makedirs("ml", exist_ok=True)
joblib.dump(scaler,"ml/memory_scaler.pkl")

# -------------------------------
# CREATE SEQUENCES
# -------------------------------

sequences = []

for i in range(len(values_scaled) - SEQ_LEN):
    sequences.append(values_scaled[i:i+SEQ_LEN])

X = np.array(sequences)

print("Training shape:",X.shape)

# -------------------------------
# MODEL
# -------------------------------

inputs = Input(shape=(SEQ_LEN,1))

encoded = LSTM(64,activation="tanh")(inputs)

decoded = RepeatVector(SEQ_LEN)(encoded)

decoded = LSTM(64,activation="tanh",return_sequences=True)(decoded)

model = Model(inputs,decoded)

optimizer = Adam(learning_rate=0.001,clipnorm=1.0)

model.compile(optimizer=optimizer,loss="mse")

model.summary()

# -------------------------------
# TRAIN
# -------------------------------

early_stop = EarlyStopping(
    monitor="loss",
    patience=5,
    restore_best_weights=True
)

model.fit(
    X,
    X,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    shuffle=True,
    callbacks=[early_stop]
)

model.save("ml/memory_lstm_model.keras")

print("[SUCCESS] Memory model saved")
