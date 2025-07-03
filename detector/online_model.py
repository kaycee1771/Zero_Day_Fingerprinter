from river import anomaly
from river import drift
import joblib
import os

class OnlineZeroDayDetector:
    def __init__(self):
        self.model = anomaly.HalfSpaceTrees(seed=42, n_trees=10, height=5, window_size=50)
        self.drift_detector = drift.ADWIN()
        self.alert_history = []

    def update(self, behavior_vector: dict):
        if self.model is None:
            return None

        vector = {
            "syscall_rate": float(behavior_vector["syscall_rate"]),
            "avg_entropy": float(behavior_vector["avg_entropy"]),
            "fork_rate": float(behavior_vector["fork_rate"]),
            "zombie_count": float(behavior_vector["zombie_count"])
        }

        score = float(self.model.score_one(vector))
        self.model = self.model.learn_one(vector)
        drift_status = bool(self.drift_detector.drift_detected)

        result = {
            "score": score,
            "drift": drift_status,
            "vector": vector
        }

        if score > 3.5 or drift_status:
            self.alert_history.append(result)
            return result

        return None


    def save(self, path="models/online_model.pkl"):
        joblib.dump((self.model, self.drift_detector, self.alert_history), path)

    def load(self, path="models/online_model.pkl"):
        if os.path.exists(path):
            self.model, self.drift_detector, self.alert_history = joblib.load(path)
