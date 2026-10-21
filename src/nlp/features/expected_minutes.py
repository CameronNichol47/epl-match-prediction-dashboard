def get_expected_minutes(player_name):
    ...

import requests
import unicodedata

URL = "https://www.fotmob.com/api/data/playerData"

def normalize_name(name):
    name = unicodedata.normalize("NFKD", name)

    return "".join(
        char for char in name
        if not unicodedata.combining(char)
    ).lower()

def search_player(player_name, team_name):
    url = "https://www.fotmob.com/api/data/search/suggest"

    response = requests.get(
        url,
        params={"term": player_name, "hits": 10, "lang": "en"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )

    response.raise_for_status()
    results = response.json()

    for group in results:
        if group["title"]["key"] == "players":
            for player in group["suggestions"]:
                if (
                    normalize_name(player["name"]) == normalize_name(player_name)
                    and normalize_name(player["teamName"]) == normalize_name(team_name)
                ):
                    return int(player["id"])

    return None

def get_player_data(player_id):
    response = requests.get(
        URL,
        params={"id": player_id},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )

    response.raise_for_status()

    return response.json()

def get_expected_minutes(player_name, team_name):
    player_id = search_player(player_name, team_name)

    if player_id is None:
        return None

    data = get_player_data(player_id)
    sum_min = 0
    count = 0

    for match in data["recentMatches"]:
        if match["leagueName"] == "Premier League":
            sum_min += match["minutesPlayed"]
            count += 1

            if count == 5:
                break



    return round(sum_min / 5.0, 3)


if __name__ == "__main__":
    results = get_expected_minutes("Mateo Kovacic", "Manchester City")

    print(results)
