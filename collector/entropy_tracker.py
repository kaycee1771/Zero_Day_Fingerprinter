import os
import math

def shannon_entropy(data):
    if not data:
        return 0
    frequency = {}
    for byte in data:
        frequency[byte] = frequency.get(byte, 0) + 1
    entropy = 0
    for freq in frequency.values():
        p = freq / len(data)
        entropy -= p * math.log2(p)
    return entropy

def monitor_entropy(target_dir='/tmp'):
    """Compute average entropy of files in target_dir."""
    entropies = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            try:
                path = os.path.join(root, file)
                with open(path, 'rb') as f:
                    data = f.read(1024) 
                    entropies.append(shannon_entropy(data))
            except Exception:
                continue

    return round(sum(entropies) / len(entropies), 2) if entropies else 0
