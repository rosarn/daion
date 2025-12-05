# src/utils/utils.py
def safe_get(d, key, default=None):
    return d.get(key, default)
