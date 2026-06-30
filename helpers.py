from constants import weights
import math

def calculate_score(stats):
    performance = (calculate_winrate(stats)) * weights["winrate"] + (calculate_average_leetify_rating(stats)) * weights["leetify_rating"]
    confidence = 1 - math.exp(-stats["games"] / 20)
    return performance * confidence

def calculate_winrate(stats):
    return (stats["wins"] / stats["games"]) if stats["games"] > 0 else 0

def calculate_average_leetify_rating(stats):
    return (stats['totalRating'] / stats["games"]) if stats["games"] > 0 else 0

