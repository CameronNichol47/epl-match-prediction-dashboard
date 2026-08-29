import requests
import json

LEAGUE_ID = 4328
ROUND = 2
SEASON = "2026-2027"

url = (
    "https://www.thesportsdb.com/api/v1/json/123/"
    f"eventsround.php?id={LEAGUE_ID}&r={ROUND}&s={SEASON}"
)

response = requests.get(url, timeout=10)
response.raise_for_status()

data = response.json()

gameweek = data.get("events") or []

gameweek = sorted(
    gameweek,
    key=lambda event: (
        event.get("dateEvent", ""),
        event.get("strTime", "")
    )
)

print("Number of games:", len(gameweek))
print(json.dumps(gameweek, indent=4))