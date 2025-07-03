import psutil

def track_processes():
    fork_rate = 0
    zombie_count = 0
    parent_map = {}

    for proc in psutil.process_iter(['pid', 'ppid', 'status']):
        try:
            if proc.info['status'] == psutil.STATUS_ZOMBIE:
                zombie_count += 1

            parent = proc.info['ppid']
            parent_map[parent] = parent_map.get(parent, 0) + 1
        except Exception:
            continue

    for forks in parent_map.values():
        if forks > 1:
            fork_rate += forks

    return {
        "fork_rate": fork_rate,
        "zombie_count": zombie_count
    }
