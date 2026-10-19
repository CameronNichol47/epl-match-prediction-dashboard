
import pandas as pd
import requests
from bs4 import BeautifulSoup
from classify_availability import classify_sentences

def extract_injuries(text, team):
    injuries = []

    injury_types = [
        "knee", "ankle", "calf",
        "hamstring", "quad", "muscle",
        "fitness"
    ]

    text = text.replace("\n", " ")
    text = text.replace(" and ", ", ")

    players = text.split(",")

    for player in players:
        player = player.strip()

        if "(" not in player or ")" not in player:
            continue

        name = player.split("(")[0].strip()
        injury = player.split("(")[1].split(")")[0].strip()

        if injury.lower() in injury_types:
            injuries.append({
                "team": team,
                "player": name,
                "injury": injury.lower(),
                "status": "unknown"
            })

    return injuries

def get_team_news(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    heading = soup.find(
        lambda tag: tag.name in ["h2", "h3"]
        and tag.get_text(" ", strip=True).lower() == "team news"
    )

    if heading is None:
        raise ValueError("Team News heading not found")

    paragraphs = []

    for element in heading.find_all_next():
        if element.name in ["h2", "h3"]:
            break

        if element.name == "p":
            paragraphs.append(
                element.get_text(" ", strip=True)
            )

    return "\n".join(paragraphs)



url = (
    "https://www.sportsmole.co.uk/football/spurs/preview/"
    "spurs-vs-coventry-prediction-team-news-lineups_607110.html"
)

text = get_team_news(url)

results = classify_sentences(text)

for result in results:
    print("Status:", result["status"])
    print("Score:", result["score"])
    print("Sentence:", result["sentence"])
    print()
