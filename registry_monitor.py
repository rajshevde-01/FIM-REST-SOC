import winreg
import hashlib

registry_baseline = {}

def hash_value(value):
    return hashlib.sha256(str(value).encode()).hexdigest()

def read_registry_values(root, path):
    data = {}
    try:
        with winreg.OpenKey(root, path) as key:
            i = 0
            while True:
                name, value, _ = winreg.EnumValue(key, i)
                data[name] = hash_value(value)
                i += 1
    except OSError:
        pass
    return data

def scan_registry(paths):
    current = {}

    for path in paths:
        values = read_registry_values(winreg.HKEY_CURRENT_USER, path)
        for name, h in values.items():
            full_key = f"HKCU\\{path}\\{name}"
            current[full_key] = h

    return current, registry_baseline
