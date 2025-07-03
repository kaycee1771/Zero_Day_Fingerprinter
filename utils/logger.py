import logging
import os
import json
from datetime import datetime

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename='logs/runtime.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
    return logging.getLogger(__name__)

def default_converter(o):
    """Convert non-serializable objects to serializable format."""
    if isinstance(o, (bool, int, float, str)):
        return o
    if hasattr(o, "__float__"):
        return float(o)
    if hasattr(o, "__int__"):
        return int(o)
    return str(o)

def save_alert(alert_data):
    path = "logs/alerts.json"
    os.makedirs("logs", exist_ok=True)

    # Load old alerts
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                old = json.load(f)
        else:
            old = []
    except Exception:
        old = []

    old.append(alert_data)

    # Save with safe serialization
    with open(path, "w") as f:
        json.dump(old, f, indent=2, default=default_converter)

def log_iso_event(event_type, details, path='logs/audit_trail.log'):
    os.makedirs("logs", exist_ok=True)
    entry = {
        "time": datetime.utcnow().isoformat(),
        "event": event_type,
        "details": details
    }

    with open(path, 'a') as f:
        f.write(json.dumps(entry, default=default_converter) + "\n")
