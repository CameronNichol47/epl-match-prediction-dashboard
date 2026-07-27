import requests
import json 
LEAGUE_ID = 4328
SEASON = "2026-2027"

url = (
    "https://www.thesportsdb.com/api/v1/json/123/"
    f"eventsseason.php?id={LEAGUE_ID}&s={SEASON}"
)

response = requests.get(url, timeout=10)
response.raise_for_status()

data = response.json()
events = data.get("events") or []

events = sorted(
    events,
    key=lambda event: (
        event.get("dateEvent", ""),
        event.get("strTime", "")
    )
)

gameweek_one = events[:10]

print(json.dumps(gameweek_one[0], indent=4))