
import pandas as pd
from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = [
    "The player is unavailable due to injury",
    "The player is doubtful for the match",
    "The player is available to play",
    "The player is suspended",
    "The player is returning from injury"
]

def classify_players(players):
    results = []

    for player in players:
        prediction = classifier(
            player["text"],
            candidate_labels=labels,
            hypothesis_template="{}"
        )

        results.append({
            "player": player["player"],
            "status": prediction["labels"][0],
            "score": round(prediction["scores"][0], 3)
        })

    return results


def classify_sentences(text):
    sentences = [
        sentence.strip()
        for sentence in text.replace("\n", " ").split(".")
        if sentence.strip()
    ]

    results = []

    for sentence in sentences:
        prediction = classifier(
            sentence,
            candidate_labels=labels,
            hypothesis_template="{}"
        )

        results.append({
            "sentence": sentence,
            "status": prediction["labels"][0],
            "score": round(prediction["scores"][0], 3)
        })

    return results

players = [
    {
        "player": "Pedro Porro",
        "text": "Pedro Porro will not return from his muscular problem just yet."
    },
    {
        "player": "Dejan Kulusevski",
        "text": "Dejan Kulusevski has been cleared to make the bench."
    }
]

for result in classify_players(players):
    print(result)