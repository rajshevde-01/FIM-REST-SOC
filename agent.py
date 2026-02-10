import time
import requests
from datetime import datetime

from config import (
    AGENT_ID,
    SERVER_URL,
    MONITOR_PATH,
    SCAN_INTERVAL,
    REGISTRY_KEYS
)

from monitor import scan_directory, baseline
from registry_monitor import scan_registry, registry_baseline


def send_alert(change, target, old_hash, new_hash):
    payload = {
        "agent_id": AGENT_ID,
        "file": target,
        "change": change,
        "old_hash": old_hash,
        "new_hash": new_hash,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        requests.post(SERVER_URL, json=payload, timeout=3)
    except Exception as e:
        print("[!] Failed to send alert:", e)


print("[*] FIM Agent started (File + Registry Monitoring)")

while True:
    # ================= FILE FIM =================
    current_files, baseline_files = scan_directory(MONITOR_PATH)

    # Created / Modified files
    for file_path, new_hash in current_files.items():
        if file_path not in baseline_files:
            print(f"[FILE ALERT] CREATED → {file_path}")
            send_alert("CREATED", file_path, None, new_hash)

        elif baseline_files[file_path] != new_hash:
            print(f"[FILE ALERT] MODIFIED → {file_path}")
            send_alert("MODIFIED", file_path, baseline_files[file_path], new_hash)

    # Deleted files
    for file_path in list(baseline_files.keys()):
        if file_path not in current_files:
            print(f"[FILE ALERT] DELETED → {file_path}")
            send_alert("DELETED", file_path, baseline_files[file_path], None)

    baseline.clear()
    baseline.update(current_files)

    # ================= REGISTRY FIM =================
    current_registry, baseline_registry = scan_registry(REGISTRY_KEYS)

    # Created / Modified registry values
    for reg_key, new_hash in current_registry.items():
        if reg_key not in baseline_registry:
            print(f"[REG ALERT] CREATED → {reg_key}")
            send_alert("REG_CREATED", reg_key, None, new_hash)

        elif baseline_registry[reg_key] != new_hash:
            print(f"[REG ALERT] MODIFIED → {reg_key}")
            send_alert(
                "REG_MODIFIED",
                reg_key,
                baseline_registry[reg_key],
                new_hash
            )

    # Deleted registry values
    for reg_key in list(baseline_registry.keys()):
        if reg_key not in current_registry:
            print(f"[REG ALERT] DELETED → {reg_key}")
            send_alert("REG_DELETED", reg_key, baseline_registry[reg_key], None)

    registry_baseline.clear()
    registry_baseline.update(current_registry)

    time.sleep(SCAN_INTERVAL)
