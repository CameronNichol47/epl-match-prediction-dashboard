import requests
from understatapi import UnderstatClient
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

if not API_KEY:
    raise ValueError("FOOTBALL_DATA_API_KEY is missing")

headers = {
    "X-Auth-Token": API_KEY
}


url = "https://api.football-data.org/v4/competitions/PL/matches?matchday=1"

headers = {
    "X-Auth-Token": API_KEY
}

understat = UnderstatClient()

matches = (
    understat
    .league("EPL")
    .get_match_data(season="2025")
)


game = next(
    m for m in matches
    if m["h"]["title"] == "Manchester City"
    and m["a"]["title"] == "Aston Villa"
)

print(game['xG']['a'])

response = requests.get(url, headers=headers)

print(response.status_code)

data = response.json()
matches = []

for match in data["matches"]:
    matches.append({
        "home": match["homeTeam"]["name"],
        "away": match["awayTeam"]["name"],
        "date": match["utcDate"]
    })
    
    
print(matches)
    


