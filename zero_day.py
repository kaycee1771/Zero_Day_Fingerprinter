import argparse
import threading
import time

from collector.syscall_logger import stream_syscalls
from collector.entropy_tracker import monitor_entropy
from collector.process_tree import track_processes
from detector.zero_day_detector import detect_zero_day
from fuzz.syscaller_fuzzer import run_fuzz_script
from utils.logger import setup_logging, save_alert, log_iso_event

logger = setup_logging()

def monitor_loop():
    logger.info("Starting Real-Time Monitoring Loop")
    while True:
        try:
            syscalls = stream_syscalls()
            entropy = monitor_entropy()
            proc_data = track_processes()

            behavior_vector = {
                "syscall_rate": syscalls,
                "avg_entropy": entropy,
                "fork_rate": proc_data['fork_rate'],
                "zombie_count": proc_data['zombie_count']
            }

            alert = detect_zero_day(behavior_vector)
            if alert:
                logger.warning("Zero-Day Behavior Detected!")
                save_alert(alert)
                log_iso_event("anomaly_detected", alert)

            time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user.")
            break
        except Exception as e:
            logger.exception(f"Error in monitor loop: {e}")
            log_iso_event("system_error", {"error": str(e)})

def fuzz_loop(fuzz_path):
    logger.info("Starting fuzz test: Entropy Bomb + Zombie Forks")
    try:
        run_fuzz_script(fuzz_path)
        logger.info("Fuzz test completed")
    except Exception as e:
        logger.error(f"Fuzzing error: {e}")
        log_iso_event("fuzz_error", {"error": str(e)})

def main():
    parser = argparse.ArgumentParser(description="Zero-Day Behavior Fingerprinter CLI")
    parser.add_argument("mode", choices=["monitor", "fuzz", "full"], help="Mode to run")
    parser.add_argument("--fuzzfile", default="fuzz/test_patterns/fuzz_script_1.json", help="Path to fuzz script")
    parser.add_argument("--delay", type=int, default=5, help="Delay before starting fuzzing (only in 'full' mode)")

    args = parser.parse_args()
    logger.info("Zero-Day Behavior Fingerprinter CLI Starting...")

    if args.mode == "monitor":
        monitor_loop()

    elif args.mode == "fuzz":
        fuzz_loop(args.fuzzfile)

    elif args.mode == "full":
        monitor_thread = threading.Thread(target=monitor_loop)
        fuzz_thread = threading.Thread(target=lambda: (time.sleep(args.delay), fuzz_loop(args.fuzzfile)))

        monitor_thread.start()
        fuzz_thread.start()

        monitor_thread.join()
        fuzz_thread.join()

if __name__ == "__main__":
    main()
