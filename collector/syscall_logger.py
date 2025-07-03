import os
import time

def stream_syscalls(duration=5):
    """Estimate system call rate by counting context switches."""
    start_time = time.time()
    switch_count = 0

    while time.time() - start_time < duration:
        try:
            for pid in filter(str.isdigit, os.listdir('/proc')):
                with open(f'/proc/{pid}/status', 'r') as f:
                    for line in f:
                        if "voluntary_ctxt_switches" in line or "nonvoluntary_ctxt_switches" in line:
                            switch_count += int(line.split(":")[1].strip())
        except Exception:
            continue
        time.sleep(0.5)

    rate = switch_count / duration
    return rate
