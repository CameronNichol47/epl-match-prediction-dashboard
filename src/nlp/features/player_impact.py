from availability_score import get_availability_score
from expected_minutes import get_expected_minutes
from player_ratings import get_player_rating

def calculate_player_impact(player):
    prob_unavailable = get_availability_score(player["status"])
    expected_minutes = get_expected_minutes(player["name"])
    player_rating = get_player_rating(player["name"])

    if (prob_unavailable is None or expected_minutes is None or player_rating is None):
        return 0

    impact = prob_unavailable * expected_minutes/90 * player_rating

    return round(impact, 3)

