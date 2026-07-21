from pathlib import Path
import pandas as pd
from understatapi import UnderstatClient

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR.parent / "raw"

def load_standard_data():
    standard_html_path = (
        RAW_DIR
        / "Arsenal Stats, Premier League _ FBref.com.html"
    )

    with standard_html_path.open("r", encoding="utf-8") as file:
        standard_tables = pd.read_html(file)

    df = standard_tables[1]

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

    return df[columns].copy()

def load_shooting_tables():
    shooting_html_path = (
        RAW_DIR
        / "Arsenal Match Logs (Shooting), All Competitions _ FBref.com.html"
    )

    with shooting_html_path.open("r", encoding="utf-8") as file:
        return pd.read_html(file)

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

def add_xg(df, team):
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

    xg_values = []
    xga_values = []

    for _, row in df.iterrows():
        opponent = row["Opponent"]

        opponent = team_name_map.get(opponent, opponent)

        venue = row["Venue"]
        comp = row["Comp"]


        if venue == "Home" and comp == "Premier League":
            game = None

            for m in matches:
                if (m["h"]["title"] == team and m["a"]["title"] == opponent):
                    game = m
                    break

            if game:
                print(game)
                print("\n")

                xg = float(game["xG"]["h"])
                xga = float(game["xG"]["a"])

                xg_values.append(xg)
                xga_values.append(xga)

            else:
                print(f"Couldn't find {team} vs {opponent}")

        elif venue == "Away" and comp == "Premier League":
            game = None

            for m in matches:
                if (m["h"]["title"] == opponent and m["a"]["title"] == team):
                    game = m
                    break

            if game:
                print(game)
                print("\n")

                xga = float(game["xG"]["h"])
                xg = float(game["xG"]["a"])

                xg_values.append(xg)
                xga_values.append(xga)

            else:
                print(f"Couldn't find {team} vs {opponent}")

    df["XG_for"] = xg_values
    df["XG_against"] = xga_values

    return df

def preprocess_data(df):
    df["Venue"] = df["Venue"].map({
        "Home": 1,
        "Away": 0
    })

    df["Result"] = df["Result"].map({
        "W": 0,
        "D": 1,
        "L": 2
    })

    return df


def main():
    df = load_standard_data()
    tables = load_shooting_tables()

    df = load_shooting(df, tables)
    df = load_shooting_against(df, tables)

    df = df[df["Comp"] == "Premier League"].copy()

    df.rename(
        columns={"Venue_x": "Venue"},
        inplace=True,
    )

    if "Venue_y" in df.columns:
        df.drop(columns=["Venue_y"], inplace=True)

    df = add_xg(df, "Arsenal")
    df = preprocess_data(df)

    output_path = BASE_DIR.parent / "processed" / "Arsenal.csv"
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()











 
        










