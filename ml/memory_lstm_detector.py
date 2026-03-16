import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

class MemoryLSTMDetector:

    def __init__(self):
        self.model = load_model("ml/memory_lstm_model.keras")
        self.scaler = joblib.load("ml/memory_scaler.pkl")
        self.sequence_length = 30
        self.threshold = 0.0377   # your calculated threshold

    def create_sequences(self, data):
        seq = []
        for i in range(len(data) - self.sequence_length):
            seq.append(data[i:i+self.sequence_length])
        return np.array(seq)

    def detect(self, df):

        memory_values = df["memory_usage"].values.reshape(-1,1)

        scaled = self.scaler.transform(memory_values)

        sequences = self.create_sequences(scaled)

        if len(sequences) == 0:
            return pd.DataFrame()

        reconstructed = self.model.predict(sequences)

        mse = np.mean(np.square(sequences - reconstructed), axis=(1,2))

        anomalies = mse > self.threshold

        result = df.iloc[self.sequence_length:].copy()
        result["anomaly_score"] = mse
        result["is_anomaly"] = anomalies

        return result[result["is_anomaly"] == True]
