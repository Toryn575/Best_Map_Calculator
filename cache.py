import json
from pathlib import Path

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

def cache_path(player_id):
    return CACHE_DIR / f"{player_id}.json"

def load_cache(player_id):
    path = cache_path(player_id)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_cache(player_id, data):
    with open(cache_path(player_id), "w") as f:
        json.dump(data, f)