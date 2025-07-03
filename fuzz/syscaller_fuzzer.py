import multiprocessing
import time
import os
import random
import json

def zombie_process():
    while True:
        time.sleep(60)

def fork_zombies(count):
    for _ in range(count):
        try:
            p = multiprocessing.Process(target=zombie_process)
            p.start()
        except Exception as e:
            print(f"[!] Failed to create zombie process: {e}")

def write_random(path, size_kb):
    with open(path, 'wb') as f:
        data = os.urandom(size_kb * 1024)
        f.write(data)

def mmap_spam():
    import mmap
    with open("tmp/fuzzmap", "wb") as f:
        f.write(b'\x00' * 4096)
    for _ in range(100):
        with open("tmp/fuzzmap", "r+b") as f:
            mm = mmap.mmap(f.fileno(), 4096)
            mm.write(os.urandom(4096))
            mm.close()

def fork_bomb(depth=2):
    for _ in range(depth):
        p = multiprocessing.Process(target=fork_zombies, args=(3,))
        p.start()

def sleep(seconds):
    time.sleep(seconds)

# Action dispatcher
ACTIONS = {
    "fork_zombies": lambda step: fork_zombies(step.get("count", 5)),
    "write_random": lambda step: write_random(step["target"], step["size_kb"]),
    "mmap_spam": lambda _: mmap_spam(),
    "fork_bomb": lambda step: fork_bomb(step.get("depth", 2)),
    "sleep": lambda step: sleep(step["seconds"])
}

def run_fuzz_script(script_path):
    print("\n Running fuzz test: Entropy Bomb + Zombie Forks")

    try:
        with open(script_path, "r") as f:
            fuzz_plan = json.load(f)

        for step in fuzz_plan:
            action = step.get("action")
            print(f"→ Executing: {action}")
            try:
                ACTIONS[action](step)
            except Exception as e:
                print(f"[!] Error in {action}: {e}")
            time.sleep(step.get("delay", 1))

    except Exception as e:
        print(f"[x] Failed to run fuzz script: {e}")
