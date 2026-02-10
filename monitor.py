import os
from hasher import hash_file

baseline = {}

def scan_directory(path):
    current_state = {}

    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            current_state[full_path] = hash_file(full_path)

    return current_state, baseline
