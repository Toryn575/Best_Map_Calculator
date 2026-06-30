from constants import weights, premier_maps, steamIds
from fetch_data import getPlayerStats
import math

def calculate_score(stats):
    performance = (calculate_winrate(stats)) * weights["winrate"] + (calculate_average_leetify_rating(stats)) * weights["leetify_rating"]
    confidence = 1 - math.exp(-stats["games"] / 20)
    return performance * confidence

def calculate_winrate(stats):
    return (stats["wins"] / stats["games"]) if stats["games"] > 0 else 0

def calculate_average_leetify_rating(stats):
    return (stats['totalRating'] / stats["games"]) if stats["games"] > 0 else 0

def calculate_stats(active_players):
    player_stats = {}
    for player_name, player_id in steamIds.items():
        player_stats[player_id] = getPlayerStats(player_id)

    map_stat_totals = {}

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

    sorted_map_stat_totals = dict(sorted(map_stat_totals.items(), key=lambda item: calculate_score(item[1]), reverse=True))
    for map_name, stats in sorted_map_stat_totals.items():
        print(f"Map: {map_name:<12} | "
              f"WinRate: {calculate_winrate(stats) * 100:<7.2f}% | "
              f"AverageleetifyRating: {calculate_average_leetify_rating(stats):<6.2f} | "
              f"Games: {stats['games']:<4} | "
              f"Score: {calculate_score(stats):<12.2f}")
    return sorted_map_stat_totals