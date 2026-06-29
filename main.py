import os
import time
import requests
from dotenv import load_dotenv

import json
from pathlib import Path

load_dotenv()



# cacheing
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





def getPlayerStats(playerid):
    # getting data cached or api
    cached = load_cache(playerid)
    if cached:
        data = cached
        print(f"using cashed data for {playerid}")
    else:
        url = "https://api-public.cs-prod.leetify.com/v3/profile/matches"

        headers = {
            "_leetify_key": os.environ.get("LEETIFY_API_KEY")
        }

        query_params = {
            "steam64_id": playerid,
            "limit": 100, # number of games
            "offset": 0
        }

        response = requests.get(url, headers=headers, params=query_params)

        if response.status_code == 200:
            data = response.json() # as a list
            save_cache(playerid, data)
            #print(data)
        else:
            print(f"Error {response.status_code}: {response.text}")
            exit(1)


    # calculate map win percentages
    map_stats = {}

    for game in data:
        map_name = game["map_name"]
        if not game["stats"]:
            continue
        if game["data_source"] == "matchmaking_wingman":
            continue
        stats = game["stats"][0]

        if map_name not in map_stats:
            map_stats[map_name] = {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "totalRating": 0
            }
        # if map_name == "de_dust2" and stats["steam64_id"] == str(76561199106982401):
        #     print(stats["leetify_rating"])

        if stats["rounds_won"] > stats["rounds_lost"]:
            map_stats[map_name]["wins"] += 1
            map_stats[map_name]["games"] += 1
            map_stats[map_name]["totalRating"] += stats["leetify_rating"] * 100
        elif stats["rounds_won"] < stats["rounds_lost"]:
            map_stats[map_name]["losses"] += 1
            map_stats[map_name]["games"] += 1
            map_stats[map_name]["totalRating"] += stats["leetify_rating"] * 100
        else:
            map_stats[map_name]["games"] += 1
            map_stats[map_name]["totalRating"] += stats["leetify_rating"] * 100

    return map_stats

# steamID64s
steamIds = {"Toryn":    76561199106982401,
            "Braidon":  76561198004823354,
            "Connor":   76561198264325977,
            "Jake":     76561198152442403,
            "Aidan":    76561198086329413,
            "Harlan":   76561198147109966,
            "Woody":    76561198981876150,
            #"Ethan":    76561198154430812,
            "Braeden":  76561198800042089,
            "Matty":    76561198084985677,
            "Joe":      76561198125951436
            }

player_stats = {}
for player_name,player_id in steamIds.items():
    player_stats[player_id] = getPlayerStats(player_id)



premier_maps = {"de_nuke", "de_ancient", "de_anubis", "de_overpass", "de_inferno", "de_dust2", "de_mirage", "de_cache"}

map_stat_totals = {}
active_players = {int}
active_players.add(steamIds["Toryn"])
active_players.add(steamIds["Aidan"])
active_players.add(steamIds["Jake"])

for player_name, maps in player_stats.items():
    if player_name not in active_players:
        continue
    for map_name, stats in maps.items():
        if map_name not in premier_maps:
            continue
        if map_name not in map_stat_totals:
            map_stat_totals[map_name] = {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "totalRating": 0
            }

        map_stat_totals[map_name]["games"] += stats["games"]
        map_stat_totals[map_name]["wins"] += stats["wins"]
        map_stat_totals[map_name]["losses"] += stats["losses"]
        map_stat_totals[map_name]["totalRating"] += stats["totalRating"]


sorted_map_stat_totals = dict(sorted(map_stat_totals.items(), key=lambda x: (x[1]["wins"] / x[1]["losses"] if x[1]["losses"] > 0 else x[1]["wins"] / 1) * 0.8 + (x[1]["totalRating"] / x[1]["games"]) * 0.2, reverse=True))
#print(sorted_map_stat_totals)
for map_name, stats in sorted_map_stat_totals.items():
    print(f"Map: {map_name} | WinRate: {stats["wins"] / stats["losses"] if stats["losses"] > 0 else stats["wins"] / 1:.2f} | leetifyRating: {stats['totalRating'] / stats["games"] if stats["games"] > 0 else stats['totalRating'] / 1:.2f} | Score: {(stats["wins"] / stats["losses"] if stats["losses"] > 0 else stats["wins"] / 1) * 0.8 + (stats["totalRating"] / stats["games"]) * 0.2}")