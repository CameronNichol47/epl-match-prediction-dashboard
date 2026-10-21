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

def get_player_rating(player_name, team_name):
    player_id = search_player(player_name, team_name)

    if player_id is None:
        return None

    data = get_player_data(player_id)

    for stat in data["mainLeague"]["stats"]:
        if stat["title"] == "Rating":
            return float(stat["value"])

    return None


if __name__ == "__main__":
    results = get_player_rating("Mateo Kovacic", "Manchester City")

    print(results)
