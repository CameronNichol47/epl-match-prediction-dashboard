import requests
import unicodedata

URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def get_fpl_data():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )
    response.raise_for_status()
    return response.json()

def format_team_name(team_name):
    aliases = {
        "Nott'm Forest": "Nottingham Forest",
        "Man City": "Manchester City",
        "Man Utd": "Manchester United",
        "Spurs": "Tottenham",
        "Newcastle": "Newcastle United",
        "Coventry City": "Coventry",
        "Hull City": "Hull",
        "Ipswich Town": "Ipswich"
    }

    return aliases.get(team_name, team_name)

def normalize_team_name(team_name):
    aliases = {
        "Manchester City": "Man City",
        "Manchester United": "Man Utd",
        "Nottingham Forest": "Nott'm Forest",
        "Tottenham Hotspur": "Spurs",
        "Wolverhampton Wanderers": "Wolves",
        "Newcastle United": "Newcastle",
        "Leeds United": "Leeds",
        "Brighton and Hove Albion": "Brighton",
        "Brighton & Hove Albion": "Brighton",
        "AFC Bournemouth": "Bournemouth"
    }

    return aliases.get(team_name, team_name)

def normalize_name(name):
    name = unicodedata.normalize("NFKD", name)

    name = "".join(
        char for char in name
        if not unicodedata.combining(char)
    )

    name = name.lower()
    name = name.replace("-", " ")
    name = name.replace("'", "")
    name = " ".join(name.split())

    return name

def extract_nickname(name):
    if "'" in name:
        parts = name.split("'")

        if len(parts) >= 3:
            return parts[1]

    return None

def get_player_team(player_name, data, fixture_teams=None):
    teams = {
        team["id"]: team["name"]
        for team in data["teams"]
    }

    search_name = normalize_name(player_name)

    exact_matches = []
    surname_matches = []

    for player in data["elements"]:
        team_name = teams.get(player["team"], "UNKNOWN")

        if fixture_teams is not None and team_name not in fixture_teams:
            continue

        full_name = (
            player["first_name"] + " " + player["second_name"]
        )

        full_normalized = normalize_name(full_name)
        web_normalized = normalize_name(player["web_name"])

        nickname = extract_nickname(full_name)

        if nickname:
            nickname = normalize_name(nickname)

        if (
            search_name == full_normalized
            or search_name == web_normalized
            or search_name == nickname
        ):
            exact_matches.append(team_name)
            continue

        surname = full_normalized.split()[-1]

        if search_name == surname:
            surname_matches.append(team_name)

    if len(exact_matches) == 1:
        return exact_matches[0]

    if len(exact_matches) > 1:
        return "UNKNOWN"

    if len(surname_matches) == 1:
        return surname_matches[0]

    return "UNKNOWN"
