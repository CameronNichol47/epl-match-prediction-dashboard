from pathlib import Path
import pandas as pd
from understatapi import UnderstatClient

BASE_DIR = Path(__file__).resolve().parent

standard_html_path = (
    BASE_DIR.parent
    / "raw"
    / "Arsenal Stats, Premier League _ FBref.com.html"
)

with standard_html_path.open("r", encoding="utf-8") as file:
    standard_tables = pd.read_html(file)

afc_df = standard_tables[1]

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

html_path = (
    BASE_DIR.parent
    / "raw"
    / "Arsenal Match Logs (Shooting), All Competitions _ FBref.com.html"
)

with html_path.open("r", encoding="utf-8") as file:
    tables = pd.read_html(file)

def load_shooting(df, tables):
    shooting_for = tables[0]

    shooting_for = shooting_for[
        [
            ("For Arsenal", "Date"),
            ("For Arsenal", "Comp"),
            ("For Arsenal", "Venue"),
            ("For Arsenal", "Opponent"),
            ("Standard", "Sh"),
            ("Standard", "SoT"),
            ("Standard", "SoT%"),
        ]
    ].copy()

    shooting_for.columns = [
        "Date",
        "Comp",
        "Venue",
        "Opponent",
        "Shots_For",
        "SoT_For",
        "SoT%_For",
    ]

    merge_columns = [
        "Date",
        "Comp",
        "Venue",
        "Opponent",
    ]

    df = df.merge(
        shooting_for,
        on=merge_columns,
        how="left",
    )

    return df

afc_df = load_shooting(afc_df, tables)


def load_shooting_against(df, tables):
    shooting_against = tables[1]    

    shooting_against = shooting_against[
        [
            ("Against Arsenal", "Date"),
            ("Against Arsenal", "Comp"),
            ("Against Arsenal", "Venue"),
            ("Against Arsenal", "Opponent"),
            ("Standard", "Sh"),
            ("Standard", "SoT"),
            ("Standard", "SoT%"),
        ]
    ].copy()

    shooting_against.columns = [
        "Date",
        "Comp",
        "Venue",
        "Opponent",
        "Shots_Against",
        "SoT_Against",
        "SoT%_Against",
    ]

    df = df.merge(
        shooting_against,
        on=[
            "Date",
            "Comp",
            "Opponent",
        ],
        how="left",
    )

    return df

afc_df = load_shooting_against(afc_df, tables)

afc_df = afc_df[afc_df["Comp"] == "Premier League"]

afc_df.rename(columns={"Venue_x": "Venue"}, inplace=True)

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









