import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

SEQ_LEN = 30

class AnomalyDetector:
    def __init__(self):
        self.model = load_model("lstm_anomaly_model.keras")
        self.scaler = MinMaxScaler()
        self.scaler_fitted = False

    def _create_sequences(self, values):
        sequences = []
        for i in range(len(values) - SEQ_LEN):
            sequences.append(values[i:i + SEQ_LEN])
        return np.array(sequences)

    def detect_metric(self, df, metric_name, threshold):
        # Safety: not enough data
        if len(df) < SEQ_LEN + 5:
            return pd.DataFrame()

        temp = df[["timestamp", "pod_name", metric_name]].rename(
            columns={metric_name: "value"}
        ).dropna()

        temp = temp.sort_values("timestamp")

        # Fit scaler once
        if not self.scaler_fitted:
            self.scaler.fit(temp[["value"]])
            self.scaler_fitted = True

        scaled = self.scaler.transform(temp[["value"]])

        sequences = self._create_sequences(scaled)

        # ✅ SHAPE: (N, 30, 1)
        sequences = sequences.reshape(sequences.shape[0], SEQ_LEN, 1)

        # Model reconstructs input
        reconstructed = self.model.predict(sequences, verbose=0)

        # ✅ VALID reconstruction error
        loss = np.mean(np.abs(reconstructed - sequences), axis=(1, 2))

        result = temp.iloc[SEQ_LEN:].copy()
        result["metric"] = metric_name
        result["anomaly_score"] = loss
        result["is_anomaly"] = loss > threshold

        return result[result["is_anomaly"]]
