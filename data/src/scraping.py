from pathlib import Path
import pandas as pd
from understatapi import UnderstatClient

BASE_DIR = Path(__file__).resolve().parent

html_path = (
    BASE_DIR.parent
    / "raw"
    / "Arsenal Stats, Premier League _ FBref.com.html"
)

with html_path.open("r", encoding="utf-8") as file:
    tables = pd.read_html(file)
    afc_df = tables[1]

for col in tables[1].columns:
    print(col)

columns = [
    "Date",
    "Comp",
    "Venue",
    "Result",
    "GF",
    "GA",
    "Opponent",
    "Poss",
]

afc_df=afc_df[columns].copy()

afc_df.to_csv('Arsenal.csv', index=False)

afc_df = pd.read_csv("Arsenal.csv")

understat = UnderstatClient()

matches = (
    understat
    .league("EPL")
    .get_match_data(season="2025")
)

team_name_map = {
    "Wolves": "Wolverhampton Wanderers",
    "Leeds United": "Leeds",
    "Nottingham": "Nottingham Forest",
    "Manchester Utd": "Manchester United",
    "Newcastle": "Newcastle United"
}

for _, row in afc_df.iterrows():
    opponent = row["Opponent"]

    opponent = team_name_map.get(opponent, opponent)

    venue = row["Venue"]
    comp = row["Comp"]

    if venue == "Home" and comp == "Premier League":
        game = next(
            (
                m for m in matches
                if m["h"]["title"] == "Arsenal"
                and m["a"]["title"] == opponent
            ),
            None,
        )

        if game:
            print(game)
            print("\n")
        else:
            print(f"Couldn't find Arsenal vs {opponent}")

    elif venue == "Away" and comp == "Premier League":
        game = next(
            (
                m for m in matches
                if m["h"]["title"] == opponent
                and m["a"]["title"] == "Arsenal"
            ),
            None,
        )

        if game:
            print(game)
            print("\n")
        else:
            print(f"Couldn't find Arsenal vs {opponent}")









