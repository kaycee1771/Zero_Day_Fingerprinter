from detector.shape_fingerprinter import BehaviorFingerprinter
from detector.online_model import OnlineZeroDayDetector

fingerprinter = BehaviorFingerprinter(method='DBSCAN')
fingerprinter.load()

online_model = OnlineZeroDayDetector()
online_model.load()

def detect_zero_day(behavior_vector):
    # Clustering
    anomaly_static = fingerprinter.predict([
        behavior_vector['syscall_rate'],
        behavior_vector['avg_entropy'],
        behavior_vector['fork_rate'],
        behavior_vector['zombie_count']
    ])

    # Streaming model
    anomaly_online = online_model.update(behavior_vector)

    if anomaly_static or anomaly_online:
        return {
            "vector": behavior_vector,
            "static_anomaly": anomaly_static,
            "online_score": anomaly_online["score"] if anomaly_online else None,
            "drift": anomaly_online["drift"] if anomaly_online else False,
            "threat_label": "zero-day-like",
            "confidence": "very high" if anomaly_online and anomaly_online["drift"] else "high"
        }
    return None
