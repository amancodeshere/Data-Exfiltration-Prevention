# anomaly_detection.py
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.01)  # Adjust contamination level as needed
        self.data = []

    def fit(self, data):
        self.data = data
        self.model.fit(data)

    def predict(self, packet_features):
        prediction = self.model.predict([packet_features])
        return prediction[0] == -1  # Return True if anomaly detected
