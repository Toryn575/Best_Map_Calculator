import os
import requests
from cache import load_cache, save_cache

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

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            exit(1)

        data = response.json()  # as a list
        save_cache(playerid, data)


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