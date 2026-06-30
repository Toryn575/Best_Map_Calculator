import json
from pathlib import Path
import time

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
Cache_TTL = 60 * 60 * 12 # 12 hours

def cache_path(player_id):
    return CACHE_DIR / f"{player_id}.json"

def load_cache(player_id):
    path = cache_path(player_id)
    if not path.exists():
        return None
    with open(path, "r") as f:
        payload = json.load(f)
    timestamp = payload.get("timestamp", 0)
    data = payload.get("Data")
    if time.time() - timestamp > Cache_TTL:
        return None
    return data

def save_cache(player_id, data):
    payload = {
        "timestamp": time.time(),
        "Data": data
        }

    with open(cache_path(player_id), "w") as f:
        json.dump(payload, f)