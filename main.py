import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def getPlayerStats(playerid):
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

        if stats["rounds_won"] > stats["rounds_lost"]:
            map_stats[map_name]["wins"] += 1
            map_stats[map_name]["games"] += 1
            map_stats[map_name]["totalRating"] += stats["leetify_rating"]
        elif stats["rounds_won"] < stats["rounds_lost"]:
            map_stats[map_name]["losses"] += 1
            map_stats[map_name]["games"] += 1
            map_stats[map_name]["totalRating"] += stats["leetify_rating"]
        else:
            map_stats[map_name]["games"] += 1
            map_stats[map_name]["totalRating"] += stats["leetify_rating"]

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
for player_name,playerid in steamIds.items():
    player_stats[player_name] = getPlayerStats(playerid)

print(player_stats["Toryn"])
# premier_maps = {"de_nuke", "de_ancient", "de_anubis", "de_overpass", "de_inferno", "de_dust2", "de_mirage"}
#
# for player_stats, stats in map_stats.items():
#     if map_name not in premier_maps:
#         continue
#
#     win_rate = stats["wins"] / (stats["wins"] + stats["losses"])
#     avg_rating = stats["totalRating"] / stats["games"]
#
#     print(
#         f"{map_name}: "
#         f"{stats['wins']}-{stats['losses']} "
#         f"Win Rate: {win_rate:.2%} "
#         f"Avg Rating: {avg_rating:.3f}"
#     )